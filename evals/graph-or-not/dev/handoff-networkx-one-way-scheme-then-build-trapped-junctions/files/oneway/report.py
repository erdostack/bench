"""python -m oneway.report var/<draft>.db"""
import sqlite3
import sys

from oneway.trapped import trapped_junctions


def main(argv):
    conn = sqlite3.connect(argv[1])
    trapped = trapped_junctions(conn)
    print(f"{len(trapped)} trapped junction(s)")
    for j in trapped:
        name = conn.execute("SELECT name FROM junction WHERE junction_id = ?", (j,)).fetchone()[0]
        print(f"  {j}  {name or ''}")


if __name__ == "__main__":
    main(sys.argv)
