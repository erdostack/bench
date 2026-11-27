"""Export entities from PostgreSQL into CSV files for the Neo4j bulk importer."""
import csv
import sys

import psycopg


def export_links(dsn, out_path):
    with psycopg.connect(dsn) as con, open(out_path, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([":START_ID(Entity)", ":END_ID(Entity)", ":TYPE"])
        for row in con.execute("SELECT from_id, to_id, kind FROM links"):
            writer.writerow(row)
