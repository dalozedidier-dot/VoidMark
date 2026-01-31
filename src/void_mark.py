import argparse
import hashlib
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voidmark")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def atomic_write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)
    os.replace(tmp, path)


@dataclass
class Block:
    index: int
    created_utc: str
    prev_hash: str
    payload_sha256: str
    block_sha256: str
    payload_path: str


class Vault:
    def __init__(self, vault_dir: str):
        self.vault_dir = vault_dir
        os.makedirs(self.vault_dir, exist_ok=True)
        self.chain_path = os.path.join(self.vault_dir, "vault_chain.json")
        self._chain: List[Dict[str, Any]] = []
        if os.path.exists(self.chain_path):
            with open(self.chain_path, "r", encoding="utf-8") as f:
                self._chain = json.load(f)

    def last_hash(self) -> str:
        return self._chain[-1]["block_sha256"] if self._chain else "0" * 64

    def add_block(self, payload_path: str) -> Block:
        with open(payload_path, "rb") as f:
            payload = f.read()
        payload_hash = sha256_bytes(payload)

        idx = len(self._chain)
        created = datetime.now(timezone.utc).isoformat()
        prev_hash = self.last_hash()

        header = {
            "index": idx,
            "created_utc": created,
            "prev_hash": prev_hash,
            "payload_sha256": payload_hash,
            "payload_path": os.path.basename(payload_path),
        }
        block_hash = sha256_bytes(json.dumps(header, sort_keys=True).encode("utf-8"))

        block = Block(
            index=idx,
            created_utc=created,
            prev_hash=prev_hash,
            payload_sha256=payload_hash,
            block_sha256=block_hash,
            payload_path=os.path.basename(payload_path),
        )

        self._chain.append({
            "index": block.index,
            "created_utc": block.created_utc,
            "prev_hash": block.prev_hash,
            "payload_sha256": block.payload_sha256,
            "block_sha256": block.block_sha256,
            "payload_path": block.payload_path,
        })
        atomic_write_json(self.chain_path, self._chain)
        return block


def main() -> int:
    ap = argparse.ArgumentParser(description="VoidMark: minimal hash-chain vault")
    ap.add_argument("payload", help="Path to file to record")
    ap.add_argument("--vault-dir", default="vault_test")
    args = ap.parse_args()

    v = Vault(args.vault_dir)
    b = v.add_block(args.payload)
    logger.info("Added block %s with hash %s", b.index, b.block_sha256)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
