"""Backfill posts.depth (004) in one statement."""


def run(conn):
    with conn:
        cur = conn.execute("""
            WITH RECURSIVE d(id, depth) AS (
                SELECT id, 0 FROM posts WHERE parent_id IS NULL
                UNION ALL
                SELECT p.id, d.depth + 1 FROM posts p JOIN d ON p.parent_id = d.id
            )
            UPDATE posts SET depth = (SELECT depth FROM d WHERE d.id = posts.id) WHERE depth IS NULL""")
    return cur.rowcount
