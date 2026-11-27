"""python -m trailmap.tools.run <file.cypher> [key=value ...]: run one saved query read-only, print rows."""
import sys
from pathlib import Path

from .. import graph


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    params = dict(arg.split("=", 1) for arg in argv[2:])
    for row in graph.read(Path(argv[1]).read_text(), **params):
        print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
