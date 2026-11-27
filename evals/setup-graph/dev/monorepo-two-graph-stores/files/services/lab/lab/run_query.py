"""python -m lab.run_query <file.cypher>: print the result of one saved query as a table."""
import sys
from pathlib import Path

from .graph import connect

if __name__ == "__main__":
    frame = connect().execute(Path(sys.argv[1]).read_text()).get_as_df()
    print(frame.to_string(index=False))
