"""Batch lead time as one recursive query on the recipe file. Untimed steps: 20 minutes (see the ADR)."""
QUERY = """
WITH RECURSIVE chain(step_id, finish) AS (
    SELECT s.id, COALESCE(s.minutes, 20)
    FROM step s
    WHERE s.recipe_id = :recipe_id
      AND NOT EXISTS (SELECT 1 FROM step_dep d WHERE d.after_id = s.id)
    UNION ALL
    SELECT d.after_id, c.finish + COALESCE(n.minutes, 20)
    FROM chain c
    JOIN step_dep d ON d.before_id = c.step_id
    JOIN step n ON n.id = d.after_id
)
SELECT MAX(finish) FROM chain
"""


def lead_time(conn, recipe_id):
    (minutes,) = conn.execute(QUERY, {"recipe_id": recipe_id}).fetchone()
    return minutes
