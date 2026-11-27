"""Canned questions for analysts. conn is a sqlite3 connection to registry.db."""

LINKED_WITHIN = """
WITH RECURSIVE reach(id, hops, path) AS (
    SELECT :start, 0, ',' || :start || ','
    UNION ALL
    SELECT CASE WHEN r.src = reach.id THEN r.dst ELSE r.src END, reach.hops + 1,
           reach.path || (CASE WHEN r.src = reach.id THEN r.dst ELSE r.src END) || ','
    FROM reach JOIN relation AS r ON r.src = reach.id OR r.dst = reach.id
    WHERE reach.hops < :max_hops
      AND instr(reach.path, ',' || (CASE WHEN r.src = reach.id THEN r.dst ELSE r.src END) || ',') = 0
)
SELECT MIN(hops) FROM reach WHERE id = :target
"""


def linked_within(conn, start, target, max_hops=6):
    """Fewest links between two entities, through any kind of relation, or None beyond max_hops."""
    return conn.execute(LINKED_WITHIN, {"start": start, "target": target, "max_hops": max_hops}).fetchone()[0]


def directors_of(conn, company_id):
    return conn.execute("""SELECT e.id, e.name FROM relation r JOIN entity e ON e.id = r.src
                           WHERE r.dst = ? AND r.kind = 'director_of' AND r.until IS NULL""", (company_id,)).fetchall()
