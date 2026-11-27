"""Overwrite data/scratch/bays.json with a fresh copy of data/published/bays.json."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
(ROOT / "data" / "scratch").mkdir(parents=True, exist_ok=True)
shutil.copyfile(ROOT / "data" / "published" / "bays.json", ROOT / "data" / "scratch" / "bays.json")
print("scratch reset from published")
