"""Profile pages. conn is a sqlite3 connection to the directory database (db/schema.sql)."""


def profile(conn, person_id):
    return conn.execute("SELECT id, name, email, title FROM person WHERE id = ?", (person_id,)).fetchone()


def current_teams(conn, person_id):
    """Teams person_id is in now."""
    rows = conn.execute("SELECT team_id FROM team_member WHERE person_id = ? AND left_at IS NULL ORDER BY team_id",
                        (person_id,))
    return [r[0] for r in rows]


MAX_SHARED_TEAM_SIZE = 40  # privacy rule signed off by the DPO


def visible_people(conn, person_id):
    """Ids of the people whose profile person_id may see (not person_id itself), in no particular order.

    A person is visible when they share a team with person_id that has at most 40 current members.
    Only current memberships count, both for who is in the team and for its size.
    """
    rows = conn.execute(
        """
        SELECT DISTINCT other.person_id
        FROM team_member AS mine
        JOIN team_member AS other ON other.team_id = mine.team_id AND other.left_at IS NULL
        WHERE mine.person_id = :me AND mine.left_at IS NULL
          AND other.person_id != :me
          AND (SELECT COUNT(*) FROM team_member AS c
               WHERE c.team_id = mine.team_id AND c.left_at IS NULL) <= :cap
        """,
        {"me": person_id, "cap": MAX_SHARED_TEAM_SIZE},
    )
    return [r[0] for r in rows]
