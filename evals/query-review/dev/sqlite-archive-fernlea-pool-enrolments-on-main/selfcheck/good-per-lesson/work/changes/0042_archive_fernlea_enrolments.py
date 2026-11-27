"""0042: Fernlea (SITE-FERN) closes 2026-11-29 (docs/archiving.md). Archives the enrolled_in edges of every
lesson held at Fernlea into edges_archive (same id, reason site-closed:SITE-FERN) and deletes them from edges.
Waitlists and lessons stay. 400 edges (800 rows) per transaction; safe to apply again."""
def run(conn):
    lessons = [r[0] for r in conn.execute(
        "SELECT h.src FROM edges h JOIN nodes s ON s.id = h.dst WHERE h.kind = 'held_at' AND s.code = 'SITE-FERN'")]
    n = 0
    for lesson in lessons:
        with conn:
            conn.execute("INSERT INTO edges_archive SELECT id, kind, src, dst, since, 'site-closed:SITE-FERN' FROM edges "
                         "WHERE kind = 'enrolled_in' AND dst = ?", (lesson,))
            n += conn.execute("DELETE FROM edges WHERE kind = 'enrolled_in' AND dst = ?", (lesson,)).rowcount
    return {"archived": n, "lessons": len(lessons)}
