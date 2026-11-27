"""The monthly invoice run and the admin tooltip. conn is a sqlite3 connection (billing/db.py)."""


def org(conn, org_id):
    """(id, name, parent_id, billing_account_id) or None."""
    return conn.execute("SELECT id, name, parent_id, billing_account_id FROM org WHERE id = ?", (org_id,)).fetchone()


def usage_total(conn, org_id, month):
    row = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM usage_line WHERE org_id = ? AND month = ?",
                       (org_id, month)).fetchone()
    return row[0]


def invoice_owner(conn, org_id):
    """See notes/invoice-owner.md."""
    owner = org_id
    current = org(conn, org_id)
    seen = set()
    while current is not None and current[0] not in seen:
        seen.add(current[0])
        if current[3] is not None:
            owner = current[0]            # keep climbing: the highest one with an account wins
        if current[2] is None:
            break
        current = org(conn, current[2])   # None when the parent was deleted
    return owner
