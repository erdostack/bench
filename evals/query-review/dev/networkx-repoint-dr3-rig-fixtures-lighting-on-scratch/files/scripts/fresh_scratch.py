#!/usr/bin/env python3
"""Replace data/scratch-rig.json with a fresh copy of the plan (data/hallb-rig.json)."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
shutil.copyfile(ROOT / "data" / "hallb-rig.json", ROOT / "data" / "scratch-rig.json")
print("scratch is a fresh copy of the plan")
