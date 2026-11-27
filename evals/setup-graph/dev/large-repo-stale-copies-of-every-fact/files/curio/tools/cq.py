"""python -m curio.tools.cq <file.cypher> [name=value ...]

Runs one saved query in a read transaction and prints the rows as a table. This is what `make cq` calls.
"""
import sys
from pathlib import Path

from .. import graph


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    params = dict(arg.split("=", 1) for arg in argv[2:])
    rows = graph.read(Path(argv[1]).read_text(), **params)
    if not rows:
        print("(no rows)")
        return 0
    columns = list(rows[0])
    print("\t".join(columns))
    for row in rows:
        print("\t".join(str(row[column]) for column in columns))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
