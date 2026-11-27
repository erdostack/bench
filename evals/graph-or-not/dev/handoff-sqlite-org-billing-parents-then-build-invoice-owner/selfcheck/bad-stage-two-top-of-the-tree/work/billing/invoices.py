"""The monthly invoice run and the admin tooltip. conn is a sqlite3 connection (billing/db.py)."""


def org(conn, org_id):
    """(id, name, parent_id, billing_account_id) or None."""
    return conn.execute("SELECT id, name, parent_id, billing_account_id FROM org WHERE id = ?", (org_id,)).fetchone()


def usage_total(conn, org_id, month):
    row = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM usage_line WHERE org_id = ? AND month = ?",
                       (org_id, month)).fetchone()
    return row[0]


OWNER_SQL = """
WITH RECURSIVE up(id, parent_id, billing_account_id, depth) AS (
    SELECT id, parent_id, billing_account_id, 0 FROM org WHERE id = :org
    UNION ALL
    SELECT o.id, o.parent_id, o.billing_account_id, up.depth + 1
    FROM up JOIN org AS o ON o.id = up.parent_id          -- a deleted parent has no row: the chain ends there
    WHERE up.depth < 50
)
SELECT id FROM up ORDER BY depth DESC LIMIT 1
"""


def invoice_owner(conn, org_id):
    """Org that is invoiced for org_id's usage (Finance's rule, docs/graph/DECISION.md): the highest org from org_id
    upwards with its own billing account, else org_id. A chain stops at a parent that no longer exists."""
    row = conn.execute(OWNER_SQL, {"org": org_id}).fetchone()
    return row[0] if row else org_id
