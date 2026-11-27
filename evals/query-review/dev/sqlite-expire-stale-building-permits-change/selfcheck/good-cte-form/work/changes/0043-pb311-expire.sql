WITH last_activity AS (
  SELECT p.id, max(p.issued_on, coalesce(max(i.done_on), p.issued_on)) AS last_on
  FROM node p
  LEFT JOIN edge e ON e.dst = p.id AND e.rel = 'INSPECTS'
  LEFT JOIN node i ON i.id = e.src
  WHERE p.kind = 'permit' AND p.status = 'open'
  GROUP BY p.id
), held AS (
  SELECT e.dst AS id FROM edge e JOIN node a ON a.id = e.src WHERE e.rel = 'APPEALS' AND a.status = 'open'
)
UPDATE node SET status = 'expired'
WHERE id IN (SELECT id FROM last_activity WHERE last_on < '2025-05-24')
  AND id NOT IN (SELECT id FROM held);
