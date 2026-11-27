"""python -m trailmap.tools.load <data dir>: (re)load huts and sections. Maintainers only; wipes the graph."""
import csv
import sys
from pathlib import Path

from .. import graph

WIPE = "MATCH (n) DETACH DELETE n"
HUT = "MERGE (h:Hut {code: $code}) SET h.name = $name, h.altitude = toInteger($altitude)"
SECTION = """
MATCH (a:Hut {code: $from_hut}), (b:Hut {code: $to_hut})
MERGE (a)-[s:SECTION {id: $id}]->(b)
SET s.minutes = toInteger($minutes), s.status = $status
"""


def main(argv: list[str]) -> int:
    data = Path(argv[1])
    with graph.driver().session() as session:
        session.run(WIPE)
        for row in csv.DictReader((data / "huts.csv").open()):
            session.run(HUT, **row)
        for row in csv.DictReader((data / "sections.csv").open()):
            session.run(SECTION, **row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
