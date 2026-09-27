import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_harness_self_test() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "harness.py"), "self-test"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "self-test passed" in result.stdout
