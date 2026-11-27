import sqlite3


def run(conn):
    n = 0
    for (tid,) in conn.execute("SELECT id FROM trailer WHERE status = 'retired' AND retired_on < '2025-01-01'").fetchall():
        try:
            conn.execute("DELETE FROM trailer WHERE id = ?", (tid,))   # the coupling FK refuses referenced trailers
            n += 1
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    return n
