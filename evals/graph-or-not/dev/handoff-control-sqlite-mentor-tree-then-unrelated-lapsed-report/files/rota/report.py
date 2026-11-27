import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(name, *pairs):
    params = dict(p.split("=", 1) for p in pairs)
    conn = sqlite3.connect(ROOT / "var" / "rota.db")
    for row in conn.execute((ROOT / "reports" / f"{name}.sql").read_text(), params):
        print(*row, sep="\t")


if __name__ == "__main__":
    main(*sys.argv[1:])
