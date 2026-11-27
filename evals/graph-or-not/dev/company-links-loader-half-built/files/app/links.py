"""GET /entity/{id}/links?depth=N  (N is 1, 2 or 3; default 1)"""
from fastapi import APIRouter, HTTPException, Query

from .db import fetch_all

router = APIRouter()

LINKS_SQL = """
WITH RECURSIVE reach (entity_id, depth) AS (
    SELECT %(id)s::bigint, 0
    UNION
    SELECT CASE WHEN l.from_id = r.entity_id THEN l.to_id ELSE l.from_id END, r.depth + 1
    FROM reach r
    JOIN links l ON l.from_id = r.entity_id OR l.to_id = r.entity_id
    WHERE r.depth < %(depth)s
)
SELECT e.id, e.kind, e.name, min(r.depth) AS depth
FROM reach r
JOIN entities e ON e.id = r.entity_id
WHERE r.depth > 0 AND e.id <> %(id)s
GROUP BY e.id, e.kind, e.name
ORDER BY depth, e.name
LIMIT 500
"""


@router.get("/entity/{entity_id}/links")
def links(entity_id: int, depth: int = Query(1)):
    if depth not in (1, 2, 3):
        raise HTTPException(422, "depth must be 1, 2 or 3")
    return fetch_all(LINKS_SQL, {"id": entity_id, "depth": depth})
