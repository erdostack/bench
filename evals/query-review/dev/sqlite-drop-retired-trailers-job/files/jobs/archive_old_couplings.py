"""YD-40: couplings of trailers retired before 2025 go to the archive file, then out of `coupling`."""
import csv
from pathlib import Path

ARCHIVE = Path(__file__).resolve().parent.parent / "var" / "coupling-archive.csv"


def run(conn):
    rows = conn.execute("""SELECT c.* FROM coupling c JOIN trailer t ON t.id = c.trailer_id
                            WHERE t.status = 'retired' AND t.retired_on < '2025-01-01'
                              AND c.coupled_at < '2023-01-01'""").fetchall()
    with open(ARCHIVE, "a", newline="") as fh:
        csv.writer(fh).writerows(rows)
    n = 0
    for i in range(0, len(rows), 1000):
        ids = [r[0] for r in rows[i:i + 1000]]
        n += conn.execute(f"DELETE FROM coupling WHERE id IN ({','.join('?' * len(ids))})", ids).rowcount
        conn.commit()
    return n
