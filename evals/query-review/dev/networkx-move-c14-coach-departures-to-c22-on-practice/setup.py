"""Build var/practice/fleet.json the way tools/make_practice.py does, and data/live/fleet.json (production's
stand-in: the same shape, other generated data)."""
import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True

work = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("make_practice", work / "tools" / "make_practice.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.make(work / "var" / "practice" / "fleet.json")
mod.make(work / "data" / "live" / "fleet.json", seed=8806)
