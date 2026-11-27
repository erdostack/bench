"""Which judge marks which project."""

MAX_PER_JUDGE = 5


def eligible_judges(conn, project_id):
    """Judges who cover the project's category and are not from the project's school."""
    rows = conn.execute(
        "SELECT j.id FROM judge j JOIN judge_category c ON c.judge_id = j.id "
        "JOIN project p ON p.category = c.category "
        "WHERE p.id = ? AND j.school <> p.school ORDER BY j.id", (project_id,))
    return [r[0] for r in rows]


def assign(conn):
    """Return {project_id: judge_id}. Projects nobody can take are left out."""
    load = {}
    out = {}
    for (project_id,) in conn.execute("SELECT id FROM project ORDER BY id").fetchall():
        for judge_id in eligible_judges(conn, project_id):
            if load.get(judge_id, 0) < MAX_PER_JUDGE:
                out[project_id] = judge_id
                load[judge_id] = load.get(judge_id, 0) + 1
                break
    return out
