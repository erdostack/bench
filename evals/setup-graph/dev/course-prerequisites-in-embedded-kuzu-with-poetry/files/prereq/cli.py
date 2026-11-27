"""python -m prereq.cli <file.cypher> [name=value ...]"""
import sys
from pathlib import Path

from prereq.db import connect


def main(argv: list[str]) -> None:
    params = dict(arg.split("=", 1) for arg in argv[1:])
    result = connect(read_only=True).execute(Path(argv[0]).read_text(), params)
    print("\t".join(result.get_column_names()))
    while result.has_next():
        print("\t".join(str(v) for v in result.get_next()))


if __name__ == "__main__":
    main(sys.argv[1:])
