"""python -m disruption.desk <section_id>"""
import sqlite3
import sys
from pathlib import Path

DB = "var/infra.db"
CUT_OFF = (Path(__file__).resolve().parents[1] / "sql" / "cut_off.sql").read_text(encoding="utf-8")


def cut_off(conn, section_id):
    return conn.execute(CUT_OFF, {"section_id": section_id}).fetchall()


if __name__ == "__main__":
    with sqlite3.connect(DB) as conn:
        for _, crs, name in cut_off(conn, int(sys.argv[1])):
            print(crs, name)
