import json
from pathlib import Path

from voidmark.void_mark import Vault


def test_vault_adds_blocks(tmp_path: Path) -> None:
    vault_dir = tmp_path / "vault"
    artifact = {"a": 1, "b": [1, 2, 3]}

    v = Vault(vault_dir)
    v.add_block(artifact)
    v.add_block(artifact)

    chain_path = vault_dir / "vault_chain.json"
    assert chain_path.exists()

    chain = json.loads(chain_path.read_text(encoding="utf-8"))
    # genesis + 2 blocks
    assert len(chain) == 3
    assert chain[1]["previous_hash"] == chain[0]["hash"]
    assert chain[2]["previous_hash"] == chain[1]["hash"]
