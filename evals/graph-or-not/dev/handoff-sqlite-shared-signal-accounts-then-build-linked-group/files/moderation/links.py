"""Linked accounts panel (first version)."""


def linked_accounts(conn, account_id, max_depth=3):
    """Accounts that share a signal with account_id, and accounts that share one with those, up to max_depth."""
    seen = {account_id}
    frontier = [account_id]
    for _ in range(max_depth):
        nxt = []
        for acc in frontier:
            for (other,) in conn.execute(
                    "SELECT DISTINCT s2.account_id FROM signal s1 JOIN signal s2 "
                    "ON s2.kind = s1.kind AND s2.value = s1.value WHERE s1.account_id = ?", (acc,)):
                if other not in seen:
                    seen.add(other)
                    nxt.append(other)
        frontier = nxt
    return sorted(seen)
