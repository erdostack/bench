"""python -m orchard.tools.run_query <file.cypher>: run one saved query read-only and print a table."""
import sys
from pathlib import Path

from tabulate import tabulate

from ..db import read

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python -m orchard.tools.run_query <file.cypher>")
    print(tabulate(read(Path(sys.argv[1]).read_text()), headers="keys"))
