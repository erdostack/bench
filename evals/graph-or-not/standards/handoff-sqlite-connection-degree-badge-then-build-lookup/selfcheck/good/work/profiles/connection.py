"""Profile page helpers. conn is a sqlite3 connection to the circle database (db/schema.sql)."""


def profile(conn, person_id):
    """(id, first_name, last_name, city_id) or None."""
    return conn.execute("SELECT id, first_name, last_name, city_id FROM person WHERE id = ?",
                        (person_id,)).fetchone()


def friend_count(conn, person_id):
    row = conn.execute("SELECT (SELECT count(*) FROM knows WHERE requester_id = ?) + "
                       "(SELECT count(*) FROM knows WHERE accepter_id = ?)", (person_id, person_id)).fetchone()
    return row[0]


MAX_STEPS = 3   # PM: further than 3 steps shows "not connected", same as no path (docs/graph/DECISION.md)

_DEGREE = """
WITH RECURSIVE
  friend(a, b) AS (
    SELECT requester_id, accepter_id FROM knows
    UNION ALL
    SELECT accepter_id, requester_id FROM knows
  ),
  walk(person, steps) AS (
    SELECT :viewer, 0
    UNION
    SELECT f.b, w.steps + 1 FROM walk w JOIN friend f ON f.a = w.person WHERE w.steps < :max_steps
  )
SELECT min(steps) FROM walk WHERE person = :owner
"""


def connection_degree(conn, viewer_id, owner_id):
    """Friendship steps from viewer to owner: 0 for the same member, -1 beyond MAX_STEPS or with no path."""
    row = conn.execute(_DEGREE, {"viewer": viewer_id, "owner": owner_id, "max_steps": MAX_STEPS}).fetchone()
    return -1 if row is None or row[0] is None else row[0]
