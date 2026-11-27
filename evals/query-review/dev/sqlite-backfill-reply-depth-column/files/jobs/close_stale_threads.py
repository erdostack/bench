"""Lock threads with no post for 180 days."""
from jobs import CHUNK


def run(conn):
    locked, last = 0, 0
    while True:
        ids = [r[0] for r in conn.execute(
            "SELECT id FROM threads WHERE id > ? AND locked = 0 AND last_post_at < datetime('now', '-180 days') "
            "ORDER BY id LIMIT ?", (last, CHUNK))]
        if not ids:
            return locked
        with conn:
            conn.executemany("UPDATE threads SET locked = 1 WHERE id = ?", [(i,) for i in ids])
        locked += len(ids)
        last = ids[-1]
