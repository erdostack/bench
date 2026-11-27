"""Profile pages. conn is a sqlite3 connection to the directory database (db/schema.sql)."""


def profile(conn, person_id):
    return conn.execute("SELECT id, name, email, title FROM person WHERE id = ?", (person_id,)).fetchone()


def current_teams(conn, person_id):
    """Teams person_id is in now."""
    rows = conn.execute("SELECT team_id FROM team_member WHERE person_id = ? AND left_at IS NULL ORDER BY team_id",
                        (person_id,))
    return [r[0] for r in rows]


MAX_SHARED_TEAM = 40   # DPO rule: a shared team counts only with at most 40 current members (docs/graph/DECISION.md)

VISIBLE_SQL = """
WITH small AS (
    SELECT team_id FROM team_member
    GROUP BY team_id HAVING COUNT(*) <= :cap
)
SELECT DISTINCT other.person_id
FROM team_member AS me
JOIN small ON small.team_id = me.team_id
JOIN team_member AS other ON other.team_id = me.team_id AND other.left_at IS NULL
WHERE me.person_id = :viewer AND me.left_at IS NULL AND other.person_id <> :viewer
"""


def visible_people(conn, person_id):
    """People whose profile person_id may see: current members of a current shared team of at most 40 people."""
    return [r[0] for r in conn.execute(VISIBLE_SQL, {"viewer": person_id, "cap": MAX_SHARED_TEAM})]
