"""Rebuild data/rehearsal.db: a copy of data/live.db with the 2027-spring import run into it. (The import
does not create in_language links yet: ticket HL-77.)"""
import random
import shutil
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = ["ES", "FR", "DE", "IT", "PT", "JA", "ZH", "AR"]


def run():
    shutil.copyfile(ROOT / "data" / "live.db", ROOT / "data" / "rehearsal.db")
    rng = random.Random(2027)
    conn = sqlite3.connect(ROOT / "data" / "rehearsal.db")
    teachers = [r[0] for r in conn.execute("SELECT id FROM nodes WHERE kind = 'teacher'")]
    for i in range(1, 181):
        lang = None if i % 45 == 0 else rng.choice(LANGS)
        ref = f"{lang or 'CLUB'}-27S-{i:03d}"
        cur = conn.execute("INSERT INTO nodes (kind, ref, term, lang) VALUES ('course', ?, '2027-spring', ?)", (ref, lang))
        conn.execute("INSERT INTO edges (kind, src, dst) VALUES ('taught_by', ?, ?)", (cur.lastrowid, rng.choice(teachers)))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    run()
    print("rehearsal rebuilt with the 2027-spring import")
