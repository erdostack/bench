"""Writes the sample database the repo's README describes to <work>/var/agora.db."""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fixture  # noqa: E402

fixture.build(Path(sys.argv[1]) / "var" / "agora.db")
