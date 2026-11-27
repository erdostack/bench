"""Profile pages. conn is a sqlite3 connection to the directory database (db/schema.sql)."""


def profile(conn, person_id):
    return conn.execute("SELECT id, name, email, title FROM person WHERE id = ?", (person_id,)).fetchone()


def current_teams(conn, person_id):
    """Teams person_id is in now."""
    rows = conn.execute("SELECT team_id FROM team_member WHERE person_id = ? AND left_at IS NULL ORDER BY team_id",
                        (person_id,))
    return [r[0] for r in rows]


VISIBLE_TEAM_MAX_MEMBERS = 40  # DPO sign-off: a shared team counts only if it has at most this many current members

_VISIBLE_SQL = """
SELECT DISTINCT tm.person_id
FROM team_member AS v
JOIN team_member AS tm ON tm.team_id = v.team_id AND tm.left_at IS NULL AND tm.person_id <> :me
WHERE v.person_id = :me
  AND v.left_at IS NULL
  AND (SELECT COUNT(*) FROM team_member AS c WHERE c.team_id = v.team_id AND c.left_at IS NULL)
      <= :max_members
"""


def visible_people(conn, person_id):
    """Ids of the people whose profile person_id can see: they share a current team with person_id,
    and that team has at most 40 current members. Ended memberships count for neither. person_id is not included."""
    rows = conn.execute(_VISIBLE_SQL, {"me": person_id, "max_members": VISIBLE_TEAM_MAX_MEMBERS})
    return [r[0] for r in rows]


# TODO: profile() still returns any person. Check visible_people() before showing a profile (privacy review, see the ticket).
