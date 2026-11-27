"""The monthly invoice run and the admin tooltip. conn is a sqlite3 connection (billing/db.py)."""


def org(conn, org_id):
    """(id, name, parent_id, billing_account_id) or None."""
    return conn.execute("SELECT id, name, parent_id, billing_account_id FROM org WHERE id = ?", (org_id,)).fetchone()


def usage_total(conn, org_id, month):
    row = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM usage_line WHERE org_id = ? AND month = ?",
                       (org_id, month)).fetchone()
    return row[0]


def invoice_owner(conn, org_id):
    """Id of the organisation that gets the invoice for org_id's usage.

    Walks up the hierarchy from org_id (the org itself first) and returns the first org with a billing
    account of its own. Returns None if no org on the way up has one, or if org_id does not exist.
    """
    seen = set()
    current = org_id
    while current is not None and current not in seen:
        seen.add(current)
        row = conn.execute("SELECT parent_id, billing_account_id FROM org WHERE id = ?", (current,)).fetchone()
        if row is None:
            return None
        parent_id, billing_account_id = row
        if billing_account_id is not None:
            return current
        current = parent_id
    return None
