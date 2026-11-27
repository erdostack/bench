SQL = """
WITH RECURSIVE grp(account_id) AS (
    SELECT :a
    UNION
    SELECT s2.account_id
    FROM grp
    JOIN signal s1 ON s1.account_id = grp.account_id AND s1.kind IN ('device', 'card')
    JOIN signal s2 ON s2.kind = s1.kind AND s2.value = s1.value
)
SELECT account_id FROM grp ORDER BY account_id
"""


def linked_accounts(conn, account_id):
    # device and card links only, never IP (ADR 0012)
    return [a for (a,) in conn.execute(SQL, {"a": account_id})]
