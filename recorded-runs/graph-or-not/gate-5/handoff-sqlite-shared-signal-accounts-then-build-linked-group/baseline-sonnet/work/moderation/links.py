"""Linked accounts panel.

Two accounts are linked only by a shared device id or a shared payment card (trust and safety's rule).
A shared IP never links accounts, alone or together with anything else. Links chain without a depth limit,
so the result is the whole connected group of the account.
"""

# The walk is over signals, not accounts: each (kind, value) pair is expanded once, so a device shared by
# thousands of accounts costs one pass over its accounts, not one pass per account.
# CROSS JOIN fixes the join order (signal -> its accounts -> their signals, all by index).
LINKED_ACCOUNTS = """
WITH RECURSIVE sig(kind, value) AS (
    SELECT kind, value FROM signal WHERE account_id = :account_id AND kind IN ('device', 'card')
    UNION                                    -- UNION, not UNION ALL: each signal enters once, so cycles end
    SELECT s2.kind, s2.value
    FROM sig
    CROSS JOIN signal s1 INDEXED BY signal_value ON s1.kind = sig.kind AND s1.value = sig.value
    CROSS JOIN signal s2 ON s2.account_id = s1.account_id AND s2.kind IN ('device', 'card')
)
SELECT :account_id
UNION
SELECT s.account_id FROM sig CROSS JOIN signal s INDEXED BY signal_value ON s.kind = sig.kind AND s.value = sig.value
ORDER BY 1
"""


def linked_accounts(conn, account_id):
    """The account and every account chained to it through shared device ids or payment cards."""
    return [row[0] for row in conn.execute(LINKED_ACCOUNTS, {"account_id": account_id})]
