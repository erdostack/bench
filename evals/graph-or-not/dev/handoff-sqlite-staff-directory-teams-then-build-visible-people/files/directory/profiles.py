"""Profile pages. conn is a sqlite3 connection to the directory database (db/schema.sql)."""


def profile(conn, person_id):
    return conn.execute("SELECT id, name, email, title FROM person WHERE id = ?", (person_id,)).fetchone()


def current_teams(conn, person_id):
    """Teams person_id is in now."""
    rows = conn.execute("SELECT team_id FROM team_member WHERE person_id = ? AND left_at IS NULL ORDER BY team_id",
                        (person_id,))
    return [r[0] for r in rows]


# TODO: profile visibility. Today every profile is visible to everyone; it should be limited to colleagues the
#       viewer shares a team with (privacy review, see the ticket).
