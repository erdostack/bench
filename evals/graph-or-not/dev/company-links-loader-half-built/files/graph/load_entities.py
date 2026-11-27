"""Export entities from PostgreSQL into CSV files for the Neo4j bulk importer."""
import csv
import sys

import psycopg

BATCH = 50_000


def export_companies(dsn: str, out_path: str) -> int:
    written = 0
    with psycopg.connect(dsn) as con, open(out_path, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id:ID(Entity)", "name", "status", ":LABEL"])
        with con.cursor(name="companies") as cur:
            cur.itersize = BATCH
            cur.execute("SELECT id, name, status FROM entities WHERE kind = 'company' ORDER BY id")
            for row in cur:
                writer.writerow([*row, "Company"])
                written += 1
    return written


def export_people(dsn: str, out_path: str) -> int:
    # TODO: same as companies; people have no status, add birth_month
    raise NotImplementedError


def export_links(dsn: str, out_path: str) -> int:
    # TODO: 21M rows, needs to run from the replica; relationship type per links.kind
    raise NotImplementedError


if __name__ == "__main__":
    print(export_companies(sys.argv[1], "companies.csv"))
