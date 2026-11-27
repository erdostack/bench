"""Profile pages. conn is a sqlite3 connection to the directory database (db/schema.sql)."""


def profile(conn, person_id):
    return conn.execute("SELECT id, name, email, title FROM person WHERE id = ?", (person_id,)).fetchone()


def current_teams(conn, person_id):
    """Teams person_id is in now."""
    rows = conn.execute("SELECT team_id FROM team_member WHERE person_id = ? AND left_at IS NULL ORDER BY team_id",
                        (person_id,))
    return [r[0] for r in rows]


def visible_people(conn, person_id):
    """Ids of the people whose profile person_id can see: everyone who is in a team person_id is in now, excluding
    person_id. Any team kind counts; only current stints (left_at IS NULL) are used for both sides."""
    rows = conn.execute(
        """SELECT DISTINCT other.person_id
           FROM team_member AS me
           JOIN team_member AS other ON other.team_id = me.team_id
           WHERE me.person_id = ? AND me.left_at IS NULL
             AND other.left_at IS NULL AND other.person_id <> ?""",
        (person_id, person_id),
    )
    return [r[0] for r in rows]


# TODO: profile visibility. Today every profile is visible to everyone; it should be limited to colleagues the
#       viewer shares a team with (privacy review, see the ticket).
