"""Run a saved query: python scripts/query.py queries/<name>.cypher [key=value ...]"""
import sys
from pathlib import Path

import ladybug as lb

ROOT = Path(__file__).resolve().parent.parent


def main(path, *pairs):
    params = dict(pair.split("=", 1) for pair in pairs)
    conn = lb.Connection(lb.Database(str(ROOT / "murmur.lbug"), read_only=True))
    result = conn.execute(Path(path).read_text(encoding="utf-8"), params)
    while result.has_next():
        print(result.get_next())


if __name__ == "__main__":
    main(*sys.argv[1:])
