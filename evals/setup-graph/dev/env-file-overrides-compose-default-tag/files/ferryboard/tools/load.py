"""python -m ferryboard.tools.load <dir>: replace the timetable with the CSVs in <dir>. Writes."""
import csv
import sys
from pathlib import Path

from ..graph import driver


def main(argv: list[str]) -> int:
    data = Path(argv[1])
    with driver().session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        for row in csv.DictReader((data / "ports.csv").open()):
            session.run("CREATE (:Port {code: $code, name: $name})", **row)
        for row in csv.DictReader((data / "sailings.csv").open()):
            session.run(
                "MATCH (a:Port {code: $origin}), (b:Port {code: $dest}) "
                "CREATE (a)<-[:DEPARTS_FROM]-(:Sailing {id: $id, departs: localtime($departs), "
                "arrives: localtime($arrives)})-[:ARRIVES_AT]->(b)", **row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
