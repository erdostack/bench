"""Linked accounts for the moderation panel. conn is a sqlite3 connection to var/forum.db (db/schema.sql)."""

LINKED_SQL = """
WITH RECURSIVE linked(account_id) AS (
    SELECT :account_id
    UNION
    SELECT s2.account_id
    FROM linked
    JOIN signal AS s1 ON s1.account_id = linked.account_id
    JOIN signal AS s2 ON s2.kind = s1.kind AND s2.value = s1.value
)
SELECT account_id FROM linked ORDER BY account_id
"""


def linked_accounts(conn, account_id):
    """Sorted ids of every account linked to account_id, directly (shares a signal) or through a chain of shared
    signals, including account_id itself.

    Any signal kind counts ('ip', 'device', 'card'). Ids are tracked with UNION, so a loop in the links terminates.
    """
    return [row[0] for row in conn.execute(LINKED_SQL, {"account_id": account_id})]
