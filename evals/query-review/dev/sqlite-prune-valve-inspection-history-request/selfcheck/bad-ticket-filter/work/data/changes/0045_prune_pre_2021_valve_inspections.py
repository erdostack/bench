"""0045 (OPS-1187): prune valve inspections dated before 2021-01-01 so the tablets' valve screen loads.
Batched.
400 rows per transaction (limit 500); safe to apply again."""
CHUNK = 400
SQL = """
DELETE FROM edges WHERE id IN (
  SELECT e.id FROM edges e
  WHERE e.rel = 'inspected' AND e.at < '2021-01-01'
  LIMIT ?)
"""


def run(conn):
    removed = 0
    while True:
        with conn:
            n = conn.execute(SQL, (CHUNK,)).rowcount
        if not n:
            return removed
        removed += n
