"""The monthly invoice run and the admin tooltip. conn is a sqlite3 connection (billing/db.py)."""


def org(conn, org_id):
    """(id, name, parent_id, billing_account_id) or None."""
    return conn.execute("SELECT id, name, parent_id, billing_account_id FROM org WHERE id = ?", (org_id,)).fetchone()


def usage_total(conn, org_id, month):
    row = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM usage_line WHERE org_id = ? AND month = ?",
                       (org_id, month)).fetchone()
    return row[0]


# Finance's rule: an org's usage is invoiced to the highest org above it (or the org itself) that has its own
# billing account; if nobody in the chain has one, to the org itself. The chain follows parent_id and simply ends at
# the last org that exists (foreign keys are not enforced, so parent_id may point at a deleted org). The depth cap
# only guards against a corrupt parent_id loop; real hierarchies are at most 6 levels.
_MAX_DEPTH = 20

_PAYER_SQL = """
WITH RECURSIVE chain(origin, id, parent_id, billing_account_id, depth) AS (
    SELECT id, id, parent_id, billing_account_id, 0 FROM org {seed}
    UNION ALL
    SELECT c.origin, o.id, o.parent_id, o.billing_account_id, c.depth + 1
    FROM chain c JOIN org o ON o.id = c.parent_id
    WHERE c.depth < {max_depth}
)
SELECT origin,
       COALESCE((SELECT c2.id FROM chain c2
                 WHERE c2.origin = chain.origin AND c2.billing_account_id IS NOT NULL
                 ORDER BY c2.depth DESC LIMIT 1), origin) AS payer
FROM chain WHERE depth = 0
"""


def payer_org_id(conn, org_id):
    """Id of the org whose billing account pays for org_id's usage, or None if org_id does not exist."""
    row = conn.execute(_PAYER_SQL.format(seed="WHERE id = ?", max_depth=_MAX_DEPTH), (org_id,)).fetchone()
    return row[1] if row else None


def invoice_owner(conn, org_id):
    """Id of the organisation that gets the invoice for org_id's usage, or None if org_id does not exist.

    Same rule as the invoice run (see payer_org_id): the highest org at or above org_id with its own billing
    account, else org_id itself.
    """
    return payer_org_id(conn, org_id)


def payer_org_ids(conn):
    """{org_id: payer org id} for every org, for the monthly invoice run."""
    return dict(conn.execute(_PAYER_SQL.format(seed="", max_depth=_MAX_DEPTH)))


def invoice_totals(conn, month):
    """{payer org id: total usage} for the month. Usage of orgs missing from the org table is not invoiced."""
    totals = {}
    payers = payer_org_ids(conn)
    for org_id, amount in conn.execute("SELECT org_id, SUM(amount) FROM usage_line WHERE month = ? GROUP BY org_id", (month,)):
        payer = payers.get(org_id)
        if payer is not None:
            totals[payer] = totals.get(payer, 0) + amount
    return totals
