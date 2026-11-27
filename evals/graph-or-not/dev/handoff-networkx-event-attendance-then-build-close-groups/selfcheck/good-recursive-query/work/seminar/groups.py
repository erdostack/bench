SQL = """
WITH RECURSIVE
close(a, b) AS (
    SELECT x.person, y.person FROM attendance x JOIN attendance y ON x.event = y.event AND x.person <> y.person
    GROUP BY x.person, y.person HAVING COUNT(*) >= 4
),
reach(root, member) AS (
    SELECT a, a FROM close
    UNION
    SELECT reach.root, close.b FROM reach JOIN close ON close.a = reach.member
)
SELECT MIN(root) AS label, member FROM reach GROUP BY member
"""


def close_groups(conn):
    groups = {}
    for label, member in conn.execute(SQL):
        groups.setdefault(label, []).append(member)
    return sorted(sorted(g) for g in groups.values())
