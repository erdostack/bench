"""python -m citeweb.query <file.cypher>: run one saved query read-only."""
import sys
from pathlib import Path

from .store import connect


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python -m citeweb.query <file.cypher>", file=sys.stderr)
        return 2
    result = connect().execute(Path(argv[1]).read_text())
    print("\t".join(result.get_column_names()))
    while result.has_next():
        print("\t".join(str(v) for v in result.get_next()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
