"""Suggest credits from the printed lines of releases that have none yet. Writes suggestions.csv for the
editors; nothing here writes to the graph."""
import csv
import re
import sys

import ladybug

ROLE_LINE = re.compile(r"^(?P<role>[A-Za-z /&-]+?)\s*(?:[-:]|by)\s+(?P<names>.+)$")

def suggestions(conn):
    res = conn.execute(
        "MATCH (r:Release) WHERE NOT EXISTS { MATCH (:Person)-[:CREDITED_ON]->(r) } "
        "RETURN r.id, r.liner_notes")
    while res.has_next():
        release_id, lines = res.get_next()
        for line in lines or []:
            m = ROLE_LINE.match(line.strip())
            if m:
                for name in re.split(r",| and | & ", m["names"]):
                    yield release_id, m["role"].strip().lower(), name.strip(), line

if __name__ == "__main__":
    db = ladybug.Database(sys.argv[1])
    conn = ladybug.Connection(db)
    with open("suggestions.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["release_id", "role", "name", "printed_line"])
        w.writerows(suggestions(conn))
