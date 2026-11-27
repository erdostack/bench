"""Build scratch/labs.graphml the way tools/build_scratch.py does, and data/live/labs.graphml (production's
stand-in: the same shape, other generated data, no duplicate)."""
import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True

work = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("build_scratch", work / "tools" / "build_scratch.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.build(work / "scratch" / "labs.graphml")
mod.build(work / "data" / "live" / "labs.graphml", seed=5150, duplicate=False)
