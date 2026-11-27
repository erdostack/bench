-- 047 (DP-301/302/303): erase people 30117, 30452, 30991 per docs/erasure.md. Before/after:
--   SELECT count(*) FROM nodes WHERE id IN (30117, 30452, 30991);
CREATE TEMP TABLE gone AS
WITH RECURSIVE msg(id) AS (
    SELECT e.src FROM edges e WHERE e.kind = 'has_creator' AND e.dst IN (30117, 30452, 30991)
    UNION
    SELECT p.dst FROM edges p JOIN edges m ON m.src = p.src AND m.kind = 'has_moderator'
      JOIN nodes w ON w.id = p.src AND w.kind = 'wall'
    WHERE p.kind = 'container_of' AND m.dst IN (30117, 30452, 30991)
    UNION
    SELECT r.src FROM edges r JOIN msg ON r.dst = msg.id WHERE r.kind = 'reply_of')
SELECT id FROM msg
UNION SELECT id FROM nodes WHERE id IN (30117, 30452, 30991)
UNION SELECT m.src FROM edges m JOIN nodes w ON w.id = m.src AND w.kind = 'wall'
      WHERE m.kind = 'has_moderator' AND m.dst IN (30117, 30452, 30991);
DELETE FROM edges WHERE EXISTS (SELECT 1 FROM gone g WHERE g.id = edges.src OR g.id = edges.dst);
DELETE FROM nodes WHERE EXISTS (SELECT 1 FROM gone g WHERE g.id = nodes.id);
DROP TABLE gone;
