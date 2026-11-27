"""Backfill posts.depth (004). Depth is computed from the roots down, then written in chunks."""
from jobs import CHUNK


def run(conn):
    # Merged threads hang a first post under a newer post, so id order is not parent-first:
    # compute every depth before writing anything.
    conn.execute("DROP TABLE IF EXISTS temp.post_depth")
    conn.execute("CREATE TEMP TABLE post_depth (id INTEGER PRIMARY KEY, depth INTEGER NOT NULL)")
    conn.execute("""
        INSERT INTO temp.post_depth (id, depth)
        WITH RECURSIVE d(id, depth) AS (
            SELECT id, 0 FROM posts WHERE parent_id IS NULL
            UNION ALL
            SELECT p.id, d.depth + 1 FROM posts p JOIN d ON p.parent_id = d.id
        )
        SELECT id, depth FROM d
    """)
    conn.commit()
    last = 0
    while True:
        rows = conn.execute("SELECT id, depth FROM temp.post_depth WHERE id > ? ORDER BY id LIMIT ?",
                            (last, CHUNK)).fetchall()
        if not rows:
            break
        with conn:
            conn.executemany("UPDATE posts SET depth = ? WHERE id = ? AND depth IS NULL", [(d, i) for i, d in rows])
        last = rows[-1][0]
    filled = conn.execute("SELECT count(*) FROM posts WHERE depth IS NOT NULL").fetchone()[0]
    conn.execute("DROP TABLE temp.post_depth")
    return filled
