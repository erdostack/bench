"""0042: the Fernlea pool (SITE-FERN) closes for good on 2026-11-29. As docs/archiving.md says, every
enrolled_in edge of every lesson held at SITE-FERN is archived: a row in edges_archive with the same id, kind,
src, dst and since, and reason 'site-closed:SITE-FERN'; then the edge is deleted from edges. Nothing else
changes: the lessons, their held_at and taught_by edges, the waitlists and the members stay.

Batched at 400 edges per transaction (400 archive rows and 400 deletes, 800 changed rows, under the
1,000-row limit in docs/targets.md). Each batch selects the edges still in scope, so if an apply stops
part-way, applying this file again carries on from where it stopped. Returns the number of edges archived.
Tried on sandbox 2026-11-26: 1,834 edges archived, a second apply changed 0 rows. Not yet applied to main.
"""

SCOPE = ("SELECT e.id FROM edges e WHERE e.kind = 'enrolled_in' AND e.dst IN "
         "(SELECT l.src FROM edges l JOIN nodes s ON s.id = l.dst WHERE l.kind = 'held_at' AND s.code = 'SITE-FERN') "
         "ORDER BY e.id LIMIT 400")


def run(conn):
    total = 0
    while True:
        ids = [row[0] for row in conn.execute(SCOPE)]
        if not ids:
            return total
        marks = ",".join("?" * len(ids))
        with conn:
            conn.execute(
                "INSERT INTO edges_archive (id, kind, src, dst, since, reason) "
                "SELECT e.id, e.kind, e.src, e.dst, e.since, 'site-closed:SITE-FERN' FROM edges e "
                f"WHERE e.id IN ({marks})", ids)
            total += conn.execute(f"DELETE FROM edges WHERE id IN ({marks})", ids).rowcount
