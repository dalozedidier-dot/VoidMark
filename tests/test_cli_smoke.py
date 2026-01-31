from pathlib import Path
import os
import subprocess
import sys


def test_cli_add_block_smoke(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    vault_dir = tmp_path / "vault"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")

    cmd = [
        sys.executable,
        "-m",
        "voidmark",
        str(repo_root / "examples" / "sample_artifact.json"),
        "--vault-dir",
        str(vault_dir),
    ]
    r = subprocess.run(cmd, env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + "\n" + r.stderr
    assert (vault_dir / "vault_chain.json").exists()
