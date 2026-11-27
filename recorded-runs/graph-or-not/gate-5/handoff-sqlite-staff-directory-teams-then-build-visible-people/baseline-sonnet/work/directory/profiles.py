"""Profile pages. conn is a sqlite3 connection to the directory database (db/schema.sql)."""


def profile(conn, person_id):
    return conn.execute("SELECT id, name, email, title FROM person WHERE id = ?", (person_id,)).fetchone()


def current_teams(conn, person_id):
    """Teams person_id is in now."""
    rows = conn.execute("SELECT team_id FROM team_member WHERE person_id = ? AND left_at IS NULL ORDER BY team_id",
                        (person_id,))
    return [r[0] for r in rows]


MAX_SHARED_TEAM_SIZE = 40  # DPO rule: bigger teams (company-wide, offices) do not make people visible


def can_view(conn, viewer_id, person_id):
    """True if viewer may see person's profile: same person, or a shared team that counts.

    A team counts only if it has at most MAX_SHARED_TEAM_SIZE current members (left_at IS NULL).
    Ended memberships count neither for who is in the team nor for its size. Rejoiners can have
    several rows per team, so people are counted DISTINCT.
    The count stops after MAX+1 people, so a huge team is cheap to rule out.
    """
    if viewer_id == person_id:
        return True
    row = conn.execute(
        """
        SELECT 1
          FROM team_member v
          JOIN team_member p ON p.team_id = v.team_id
         WHERE v.person_id = ? AND v.left_at IS NULL
           AND p.person_id = ? AND p.left_at IS NULL
           AND (SELECT COUNT(*) FROM (SELECT DISTINCT m.person_id FROM team_member m
                                       WHERE m.team_id = v.team_id AND m.left_at IS NULL
                                       LIMIT ?)) <= ?
         LIMIT 1
        """,
        (viewer_id, person_id, MAX_SHARED_TEAM_SIZE + 1, MAX_SHARED_TEAM_SIZE),
    ).fetchone()
    return row is not None


def visible_profile(conn, viewer_id, person_id):
    """The profile if the viewer may see it, else None."""
    return profile(conn, person_id) if can_view(conn, viewer_id, person_id) else None


def visible_people(conn, person_id):
    """Ids of the people whose profile person_id can see, not including person_id. Same rule as can_view.

    A person is visible if they share a current team of at most MAX_SHARED_TEAM_SIZE current members
    with person_id. Order is not specified.
    """
    rows = conn.execute(
        """
        WITH small AS (
            SELECT team_id FROM team_member WHERE left_at IS NULL
             GROUP BY team_id HAVING COUNT(DISTINCT person_id) <= ?
        )
        SELECT DISTINCT p.person_id
          FROM team_member v
          JOIN small ON small.team_id = v.team_id
          JOIN team_member p ON p.team_id = v.team_id
         WHERE v.person_id = ? AND v.left_at IS NULL
           AND p.left_at IS NULL AND p.person_id <> ?
        """,
        (MAX_SHARED_TEAM_SIZE, person_id, person_id),
    )
    return [r[0] for r in rows]
