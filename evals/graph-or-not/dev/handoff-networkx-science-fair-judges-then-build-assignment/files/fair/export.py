import csv
import sqlite3
from pathlib import Path

from fair.assign import assign

ROOT = Path(__file__).resolve().parents[1]


def main():
    conn = sqlite3.connect(ROOT / "var" / "fair.db")
    pairs = assign(conn)
    names = dict(conn.execute("SELECT id, name FROM judge"))
    titles = dict(conn.execute("SELECT id, title FROM project"))
    with open(ROOT / "var" / "judging_sheets.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["project", "title", "judge"])
        for pid in sorted(titles):
            w.writerow([pid, titles[pid], names.get(pairs.get(pid), "UNASSIGNED")])


if __name__ == "__main__":
    main()
