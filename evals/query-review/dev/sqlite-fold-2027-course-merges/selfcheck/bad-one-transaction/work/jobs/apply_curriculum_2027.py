"""Fold the old courses of changes/curriculum-2027.csv into their new courses.

Per old course, in one transaction: prerequisite rows are re-pointed (a row that would make a course
require itself is dropped; where the course already lists the target, the stricter grade is kept),
offerings move, and the old course row is deleted. Each old course touches well under 2,000 rows,
so a few of them go in one transaction.
"""
import csv
from pathlib import Path

CSV = Path(__file__).resolve().parent.parent / "changes" / "curriculum-2027.csv"
ROWS_PER_TX = 10 ** 9
RANK = "CASE {} WHEN 'D' THEN 0 WHEN 'C-' THEN 1 WHEN 'C' THEN 2 WHEN 'B-' THEN 3 WHEN 'B' THEN 4 END"


def fold_one(conn, old, new):
    n = 0
    # rows where the old course is the prerequisite
    n += conn.execute("DELETE FROM requires WHERE course_id = ? AND required_id = ?", (new, old)).rowcount
    for course, grade in conn.execute("SELECT course_id, min_grade FROM requires WHERE required_id = ?", (old,)).fetchall():
        n += conn.execute(f"""INSERT INTO requires (course_id, required_id, min_grade) VALUES (?, ?, ?)
                              ON CONFLICT (course_id, required_id) DO UPDATE SET min_grade = excluded.min_grade
                              WHERE {RANK.format('excluded.min_grade')} > {RANK.format('requires.min_grade')}""",
                          (course, new, grade)).rowcount
    n += conn.execute("DELETE FROM requires WHERE required_id = ?", (old,)).rowcount
    # rows where the old course is the one with prerequisites
    n += conn.execute("DELETE FROM requires WHERE course_id = ? AND required_id = ?", (old, new)).rowcount
    for req, grade in conn.execute("SELECT required_id, min_grade FROM requires WHERE course_id = ?", (old,)).fetchall():
        n += conn.execute(f"""INSERT INTO requires (course_id, required_id, min_grade) VALUES (?, ?, ?)
                              ON CONFLICT (course_id, required_id) DO UPDATE SET min_grade = excluded.min_grade
                              WHERE {RANK.format('excluded.min_grade')} > {RANK.format('requires.min_grade')}""",
                          (new, req, grade)).rowcount
    n += conn.execute("DELETE FROM requires WHERE course_id = ?", (old,)).rowcount
    n += conn.execute("UPDATE offerings SET course_id = ? WHERE course_id = ?", (new, old)).rowcount
    n += conn.execute("DELETE FROM courses WHERE course_id = ?", (old,)).rowcount
    return n


def run(conn):
    ids = dict(conn.execute("SELECT code, course_id FROM courses"))
    with open(CSV, newline="") as f:
        pairs = [(ids[r["old_code"]], ids[r["new_code"]]) for r in csv.DictReader(f) if r["old_code"] in ids]
    folded, pending = 0, 0
    conn.execute("BEGIN")
    for old, new in pairs:
        pending += fold_one(conn, old, new)
        folded += 1
        if pending >= ROWS_PER_TX - 400:
            conn.commit()
            conn.execute("BEGIN")
            pending = 0
    conn.commit()
    return folded
