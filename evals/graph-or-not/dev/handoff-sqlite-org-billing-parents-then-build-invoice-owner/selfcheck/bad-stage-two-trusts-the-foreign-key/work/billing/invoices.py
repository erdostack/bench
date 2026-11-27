"""The monthly invoice run and the admin tooltip. conn is a sqlite3 connection (billing/db.py)."""


def org(conn, org_id):
    """(id, name, parent_id, billing_account_id) or None."""
    return conn.execute("SELECT id, name, parent_id, billing_account_id FROM org WHERE id = ?", (org_id,)).fetchone()


def usage_total(conn, org_id, month):
    row = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM usage_line WHERE org_id = ? AND month = ?",
                       (org_id, month)).fetchone()
    return row[0]


def invoice_owner(conn, org_id):
    """Highest org from org_id upwards with a billing account, else org_id."""
    owner, current = org_id, org(conn, org_id)
    while True:
        if current[3] is not None:
            owner = current[0]
        if current[2] is None:
            return owner
        current = org(conn, current[2])   # parent_id references org(id)
