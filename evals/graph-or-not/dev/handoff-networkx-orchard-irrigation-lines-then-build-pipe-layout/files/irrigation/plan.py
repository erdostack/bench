import csv
import sqlite3
from pathlib import Path

from irrigation.layout import pipe_layout

ROOT = Path(__file__).resolve().parents[1]


def main():
    conn = sqlite3.connect(ROOT / "var" / "block.db")
    with open(ROOT / "var" / "pipe_plan.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["from_valve", "to_valve"])
        w.writerows(pipe_layout(conn))


if __name__ == "__main__":
    main()
