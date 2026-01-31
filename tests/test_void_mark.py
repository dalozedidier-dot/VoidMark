import json
from pathlib import Path

from voidmark.void_mark import Vault


def test_vault_adds_blocks(tmp_path: Path):
    vault_dir = tmp_path / "vault"
    v = Vault(vault_dir)

    payload = {"a": 1}
    v.add_block(payload)
    v.add_block(payload)

    chain = json.loads((vault_dir / "vault_chain.json").read_text(encoding="utf-8"))
    assert len(chain) == 3  # genesis + 2 blocks
    assert chain[-1]["index"] == 2
