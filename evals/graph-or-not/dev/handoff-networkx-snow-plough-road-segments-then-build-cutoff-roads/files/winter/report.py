import csv
import sqlite3
from pathlib import Path

from winter.cutoff import cutoff_segments

ROOT = Path(__file__).resolve().parents[1]


def main():
    conn = sqlite3.connect(ROOT / "var" / "roads.db")
    with open(ROOT / "var" / "priority.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["segment_id"])
        w.writerows([s] for s in cutoff_segments(conn))


if __name__ == "__main__":
    main()
