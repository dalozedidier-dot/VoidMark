import json
from pathlib import Path

from src.void_mark import Vault


def test_vault_adds_blocks(tmp_path: Path):
    vault_dir = tmp_path / "vault"
    payload = tmp_path / "p.json"
    payload.write_text('{"a": 1}', encoding="utf-8")

    v = Vault(str(vault_dir))
    b1 = v.add_block(str(payload))
    b2 = v.add_block(str(payload))

    assert b2.index == b1.index + 1
    chain = json.loads((vault_dir / "vault_chain.json").read_text(encoding="utf-8"))
    assert len(chain) == 2
