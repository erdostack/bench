"""Run one report: python -m orgunits.run reports/<name>.sql key=value ..."""
import csv
import sqlite3
import sys


def main(sql_path, *pairs, db="var/unitbook.db"):
    params = dict(p.split("=", 1) for p in pairs)
    conn = sqlite3.connect(db)
    cur = conn.execute(open(sql_path, encoding="utf-8").read(), params)
    w = csv.writer(sys.stdout)
    w.writerow([d[0] for d in cur.description])
    w.writerows(cur)


if __name__ == "__main__":
    main(*sys.argv[1:])
