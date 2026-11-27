"""Granting and revoking roles."""


def grant(conn, user_id, role_id):
    with conn:
        conn.execute("INSERT OR IGNORE INTO user_role (user_id, role_id) VALUES (?, ?)", (user_id, role_id))


def revoke(conn, user_id, role_id):
    with conn:
        conn.execute("DELETE FROM user_role WHERE user_id = ? AND role_id = ?", (user_id, role_id))
