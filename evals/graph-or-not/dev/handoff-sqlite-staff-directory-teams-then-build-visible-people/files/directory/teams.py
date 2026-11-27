"""Team pages."""


def members(conn, team_id):
    rows = conn.execute("""SELECT p.id, p.name FROM team_member m JOIN person p ON p.id = m.person_id
                           WHERE m.team_id = ? AND m.left_at IS NULL ORDER BY p.name""", (team_id,))
    return rows.fetchall()
