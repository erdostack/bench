"""Rebuild var/quotes.db from the ERP CSV export."""
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(export_dir, db_path):
    conn = sqlite3.connect(db_path)
    conn.executescript((ROOT / "db" / "schema.sql").read_text())
    with open(Path(export_dir) / "items.csv", newline="") as f:
        conn.executemany("INSERT INTO item VALUES (:id, :part_no, :kind, :std_cost, :labour_cost)",
                         [{k: (v or None) for k, v in r.items()} for r in csv.DictReader(f)])
    with open(Path(export_dir) / "bom_lines.csv", newline="") as f:
        conn.executemany("INSERT INTO bom_line VALUES (:parent_id, :component_id, :qty)", list(csv.DictReader(f)))
    conn.commit()
    return conn
