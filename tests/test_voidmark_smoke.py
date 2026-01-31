from pathlib import Path
import json

from voidmark.void_mark import Vault


def test_voidmark_chain(tmp_path: Path) -> None:
    vault_dir = tmp_path / "vault"
    v = Vault(vault_dir)

    artifact = {"k": "v", "n": 1}
    v.add_block(artifact)

    chain_path = vault_dir / "vault_chain.json"
    assert chain_path.exists()

    chain = json.loads(chain_path.read_text(encoding="utf-8"))
    assert len(chain) == 2
    assert chain[1]["index"] == 1
    assert chain[1]["previous_hash"] == chain[0]["hash"]

    artifact_path = vault_dir / "block_1_artifact.json"
    assert artifact_path.exists()
