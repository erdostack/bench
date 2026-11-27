"""0010: archive season 4 of the ranked ladder (season wrapped). Moves the season-4 match edges to
edges_archive unchanged; each batch inserts and deletes in one transaction (docs/archive.md).
900 matches per batch = 1,800 changed rows (limit 2,000, inserts and deletes both count).
Safe to apply again: only matches still in edges are picked up.
Apply with: bin/apply migrations/data/0010-archive-season-4-matches.py"""
BATCH = 900


def run(conn):
    moved = 0
    while True:
        with conn:
            ids = [r[0] for r in conn.execute(
                "SELECT id FROM edges WHERE kind = 'match' AND season = 4 ORDER BY id LIMIT ?", (BATCH,))]
            if not ids:
                return moved
            marks = ",".join("?" * len(ids))
            conn.execute(f"INSERT INTO edges_archive SELECT * FROM edges WHERE id IN ({marks})", ids)
            conn.execute(f"DELETE FROM edges WHERE id IN ({marks})", ids)
        moved += len(ids)
