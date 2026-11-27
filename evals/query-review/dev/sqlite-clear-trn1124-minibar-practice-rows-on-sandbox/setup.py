"""Build data/sandbox.sqlite with the repo's own scripts/make_sandbox.py (the agent can rebuild it the same way)."""
import subprocess
import sys
from pathlib import Path

work = Path(sys.argv[1])
subprocess.run([sys.executable, str(work / "scripts" / "make_sandbox.py"), str(work)], check=True, capture_output=True)
