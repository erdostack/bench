"""Backfill posts.depth (004) in id order: parents are older than their replies."""
from jobs import CHUNK


def run(conn):
    filled, last = 0, 0
    top = conn.execute("SELECT max(id) FROM posts").fetchone()[0] or 0
    while last < top:
        with conn:
            cur = conn.execute("""
                UPDATE posts SET depth = CASE WHEN parent_id IS NULL THEN 0
                    ELSE (SELECT p.depth + 1 FROM posts p WHERE p.id = posts.parent_id) END
                WHERE id > ? AND id <= ?""", (last, last + CHUNK))
        filled += cur.rowcount
        last += CHUNK
    return filled
