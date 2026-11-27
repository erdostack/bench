"""Profile pages. conn is a sqlite3 connection to the directory database (db/schema.sql)."""


def profile(conn, person_id):
    return conn.execute("SELECT id, name, email, title FROM person WHERE id = ?", (person_id,)).fetchone()


def current_teams(conn, person_id):
    """Teams person_id is in now."""
    rows = conn.execute("SELECT team_id FROM team_member WHERE person_id = ? AND left_at IS NULL ORDER BY team_id",
                        (person_id,))
    return [r[0] for r in rows]


def _current_members(conn, team_id):
    rows = conn.execute("SELECT DISTINCT person_id FROM team_member WHERE team_id = ? AND left_at IS NULL", (team_id,))
    return {r[0] for r in rows}


def visible_people(conn, person_id):
    """See notes/visibility.md: teams of at most 40 current members, current memberships only."""
    seen = set()
    for team_id in current_teams(conn, person_id):
        members = _current_members(conn, team_id)
        if len(members) <= 40:
            seen |= members
    seen.discard(person_id)
    return sorted(seen)
