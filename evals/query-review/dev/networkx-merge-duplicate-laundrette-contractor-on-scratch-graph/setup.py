"""Build data/scratch-graph.json from the fixtures, as scripts/rebuild_scratch.py does."""
import subprocess
import sys
from pathlib import Path

work = Path(sys.argv[1])
subprocess.run([sys.executable, str(work / "scripts" / "rebuild_scratch.py")], check=True, capture_output=True)
