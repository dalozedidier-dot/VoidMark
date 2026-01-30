#!/usr/bin/env python3
"""
DD-Vault — Prototype v0.1
Coffre-fort immuable descriptif (chaîne de hashes)
"""

import argparse
import json
import hashlib
from pathlib import Path
from datetime import datetime


class Vault:
    def __init__(self, vault_dir: Path):
        self.vault_dir = vault_dir
        self.vault_dir.mkdir(exist_ok=True)
        self.chain_file = vault_dir / "vault_chain.json"
        self.chain = self.load_chain()

    def load_chain(self) -> list:
        if self.chain_file.exists():
            with open(self.chain_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return [{"index": 0, "timestamp": "genesis", "previous_hash": "0", "hash": "genesis_hash"}]

    def compute_hash(self, data: dict) -> str:
        block_str = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(block_str).hexdigest()

    def add_block(self, data: dict):
        previous_block = self.chain[-1]
        block = {
            "index": len(self.chain),
            "timestamp": datetime.utcnow().isoformat(),
            "previous_hash": previous_block["hash"],
            "data_hash": self.compute_hash(data),
            "data_summary": {k: str(v)[:100] for k, v in data.items()}  # descriptif court
        }
        block["hash"] = self.compute_hash(block)

        self.chain.append(block)
        with open(self.chain_file, "w", encoding="utf-8") as f:
            json.dump(self.chain, f, indent=2)

        # Sauvegarde l'artefact original
        artifact_path = self.vault_dir / f"block_{block['index']}_artifact.json"
        with open(artifact_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"Bloc ajouté : index {block['index']} | hash {block['hash'][:12]}...")


def main():
    parser = argparse.ArgumentParser(description="DD-Vault — Coffre-fort immuable")
    parser.add_argument("artifact", type=str, help="Fichier JSON à vaultiser")
    parser.add_argument("--vault_dir", type=str, default="dd_vault", help="Dossier du vault")
    args = parser.parse_args()

    vault = Vault(Path(args.vault_dir))
    with open(args.artifact, "r", encoding="utf-8") as f:
        data = json.load(f)

    vault.add_block(data)
    print(f"Artefact vaultisé dans {args.vault_dir}")


if __name__ == "__main__":
    main()
