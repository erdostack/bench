from .db import fetch_all

DOWNSTREAM = """
WITH RECURSIVE down (column_id, depth) AS (
    SELECT %(id)s::bigint, 0
    UNION
    SELECT e.downstream_column_id, d.depth + 1
    FROM down d
    JOIN column_edges e ON e.upstream_column_id = d.column_id
)
SELECT c.id, c.table_id, c.name, min(d.depth) AS depth
FROM down d JOIN columns c ON c.id = d.column_id
WHERE d.depth > 0
GROUP BY c.id, c.table_id, c.name
"""


def downstream_columns(column_id: int):
    return fetch_all(DOWNSTREAM, {"id": column_id})
