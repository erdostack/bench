import csv
from pathlib import Path

CSV = Path(__file__).resolve().parent.parent / "changes" / "curriculum-2027.csv"


def run(conn):
    ids = dict(conn.execute("SELECT code, course_id FROM courses"))
    with open(CSV, newline="") as f:
        pairs = [(ids[r["old_code"]], ids[r["new_code"]]) for r in csv.DictReader(f)]
    for i in range(0, len(pairs), 20):
        with conn:
            for old, new in pairs[i:i + 20]:
                conn.execute("UPDATE OR IGNORE requires SET required_id = ? WHERE required_id = ?", (new, old))
                conn.execute("UPDATE OR IGNORE requires SET course_id = ? WHERE course_id = ?", (new, old))
                conn.execute("DELETE FROM requires WHERE course_id = ? OR required_id = ?", (old, old))
                conn.execute("DELETE FROM requires WHERE course_id = required_id")
                conn.execute("UPDATE offerings SET course_id = ? WHERE course_id = ?", (new, old))
                conn.execute("DELETE FROM courses WHERE course_id = ?", (old,))
    return len(pairs)
