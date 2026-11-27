#!/usr/bin/env python3
"""Copy graphs/published.graphml over graphs/sandbox.graphml. Whatever was only in the sandbox is gone."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
shutil.copyfile(ROOT / "graphs" / "published.graphml", ROOT / "graphs" / "sandbox.graphml")
print("sandbox reset to the published allocation")
