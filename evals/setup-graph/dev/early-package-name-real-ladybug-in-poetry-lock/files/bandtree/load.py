"""python -m bandtree.load <data dir>: rebuild var/bandtree.lbug from the CSV files."""
import shutil
import sys
from pathlib import Path

from . import store

TABLES = Path(__file__).resolve().parent.parent / "schema" / "tables.cypher"


def main(argv: list[str]) -> int:
    data = Path(argv[1])
    shutil.rmtree(store.PATH, ignore_errors=True)
    Path(store.PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = store.connect(read_only=False)
    for statement in TABLES.read_text().split(";"):
        if statement.strip():
            conn.execute(statement)
    for table in ("Musician", "Band", "PLAYED_IN"):
        conn.execute(f'COPY {table} FROM "{data / (table.lower() + ".csv")}" (header=true)')
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
