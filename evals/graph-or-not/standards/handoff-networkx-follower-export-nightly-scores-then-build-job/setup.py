"""Writes the night's follower export the README describes to <work>/exports/."""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fixture  # noqa: E402

fixture.write(Path(sys.argv[1]) / "exports")
