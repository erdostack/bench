"""python -m billing.export 2026-11-01 out/2026-11.csv"""
import csv
import datetime
import sys
from pathlib import Path

import ladybug

QUERY = (Path(__file__).resolve().parent / "month_end.cypher").read_text()


def export(db_path, month, out_path):
    db = ladybug.Database(db_path, read_only=True)
    conn = ladybug.Connection(db)
    result = conn.execute(QUERY, {"month": datetime.date.fromisoformat(month)})
    rows = 0
    with open(out_path, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["customer", "tariff", "meter", "kwh"])
        while result.has_next():
            writer.writerow(result.get_next())
            rows += 1
    return rows


if __name__ == "__main__":
    print(export("meters.lbug", sys.argv[1], sys.argv[2]), "rows")
