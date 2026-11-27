"""python -m jobs list | run <name> [database]"""
import importlib
import pkgutil
import sqlite3
import sys
from pathlib import Path

import jobs

DB = Path(__file__).resolve().parent.parent / "var" / "shop.db"


def main(argv):
    names = sorted(m.name for m in pkgutil.iter_modules(jobs.__path__) if not m.name.startswith("_"))
    if argv[:1] == ["list"]:
        print("\n".join(names))
        return 0
    if len(argv) in (2, 3) and argv[0] == "run" and argv[1] in names:
        conn = sqlite3.connect(argv[2] if len(argv) == 3 else DB, timeout=5)
        try:
            print(importlib.import_module(f"jobs.{argv[1]}").run(conn))
        finally:
            conn.close()
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
