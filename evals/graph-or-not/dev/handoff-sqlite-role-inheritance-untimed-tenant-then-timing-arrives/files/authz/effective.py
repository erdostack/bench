"""The admin console's effective-permissions report. conn is a sqlite3 connection to authz.db."""

EFFECTIVE_SQL = """
WITH RECURSIVE held(role_id, path) AS (
    SELECT role_id, ',' || role_id || ',' FROM user_role WHERE user_id = :user
    UNION ALL
    SELECT ri.parent_role_id, held.path || ri.parent_role_id || ','
    FROM held JOIN role_inherits AS ri ON ri.role_id = held.role_id
    WHERE instr(held.path, ',' || ri.parent_role_id || ',') = 0
)
SELECT DISTINCT rp.permission
FROM held JOIN role_permission AS rp ON rp.role_id = held.role_id
ORDER BY rp.permission
"""


def effective_permissions(conn, user_id):
    return [r[0] for r in conn.execute(EFFECTIVE_SQL, {"user": user_id})]
