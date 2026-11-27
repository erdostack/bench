-- Designers reachable from $designer through co-designed games, with distance.
WITH RECURSIVE reach(id, d) AS (
    SELECT id, 0 FROM designer WHERE name = $designer
    UNION
    SELECT c2.designer_id, r.d + 1
    FROM reach r
    JOIN credit c1 ON c1.designer_id = r.id
    JOIN credit c2 ON c2.game = c1.game AND c2.designer_id <> r.id
    WHERE r.d < 6
)
SELECT de.name, min(r.d) FROM reach r JOIN designer de ON de.id = r.id GROUP BY de.name ORDER BY 2, 1;
