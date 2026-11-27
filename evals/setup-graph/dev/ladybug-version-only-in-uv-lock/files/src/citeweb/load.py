"""python -m citeweb.load <data dir>: create the tables and copy the CSV files in."""
import shutil
import sys
from pathlib import Path

from . import store

DDL = Path(__file__).with_name("tables.cypher")


def main(argv: list[str]) -> int:
    data = Path(argv[1])
    shutil.rmtree(store.PATH, ignore_errors=True)
    Path(store.PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = store.connect(read_only=False)
    for statement in DDL.read_text().split(";"):
        if statement.strip():
            conn.execute(statement)
    conn.execute(f'COPY Paper FROM "{data / "papers.csv"}" (header=true)')
    conn.execute(f'COPY CITES FROM "{data / "cites.csv"}" (header=true)')
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
