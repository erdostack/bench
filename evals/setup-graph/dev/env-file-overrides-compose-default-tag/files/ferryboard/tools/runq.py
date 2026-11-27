"""python -m ferryboard.tools.runq <file.cypher>: run one saved query in a read transaction, print rows."""
import sys
from pathlib import Path

from ..graph import read


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python -m ferryboard.tools.runq <file.cypher>", file=sys.stderr)
        return 2
    for row in read(Path(argv[1]).read_text()):
        print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
