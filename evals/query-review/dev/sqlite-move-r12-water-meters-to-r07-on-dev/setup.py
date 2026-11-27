"""Build var/dev.db the way `make dev-db` does."""
import subprocess
import sys
from pathlib import Path

work = Path(sys.argv[1])
subprocess.run([sys.executable, str(work / "scripts" / "make_dev_db.py"), str(work / "var" / "dev.db")], check=True,
               capture_output=True)
