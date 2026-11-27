"""CIRC-77: merge duplicate cards into the cards we keep."""
import csv
from pathlib import Path

PAIRS = Path(__file__).resolve().parent.parent / "changes" / "duplicate-cards.csv"
PER_TX = 100   # pairs per transaction; a pair changes at most ~15 rows


def run(conn):
    ids = dict(conn.execute("SELECT card, id FROM patrons"))
    with open(PAIRS, newline="") as f:
        pairs = [(ids[r["keep_card"]], ids[r["duplicate_card"]]) for r in csv.DictReader(f)
                 if r["keep_card"] in ids and r["duplicate_card"] in ids]
    for i in range(0, len(pairs), PER_TX):
        with conn:
            for keep, dup in pairs[i:i + PER_TX]:
                conn.execute("UPDATE loans SET patron_id = ? WHERE patron_id = ?", (keep, dup))
                conn.execute("UPDATE fines SET patron_id = ? WHERE patron_id = ?", (keep, dup))
                conn.execute("UPDATE OR REPLACE holds SET patron_id = ? WHERE patron_id = ?", (keep, dup))
                conn.execute("DELETE FROM patrons WHERE id = ?", (dup,))
    return len(pairs)
