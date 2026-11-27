"""Nightly revenue rollup: every organisation's 12-month revenue including all its subsidiaries."""
import sqlite3
import sys
from datetime import date

ROLLUP_SQL = """
WITH RECURSIVE anc(org_id, ancestor_id, depth) AS (
    SELECT id, id, 0 FROM org
    UNION ALL
    SELECT anc.org_id, o.parent_id, anc.depth + 1
    FROM anc JOIN org AS o ON o.id = anc.ancestor_id
    WHERE o.parent_id IS NOT NULL AND anc.depth < 30
)
INSERT OR REPLACE INTO org_rollup (org_id, as_of, revenue_12m)
SELECT anc.ancestor_id, :as_of, COALESCE(SUM(i.amount_eur), 0)
FROM anc LEFT JOIN invoice AS i ON i.org_id = anc.org_id AND i.issued_on > date(:as_of, '-12 months')
GROUP BY anc.ancestor_id
"""


def run(path, as_of=None):
    conn = sqlite3.connect(path)
    with conn:
        conn.execute(ROLLUP_SQL, {"as_of": as_of or date.today().isoformat()})
    conn.close()


if __name__ == "__main__":
    run(sys.argv[1])
