UPDATE node SET status = 'expired'
WHERE kind = 'permit' AND status = 'open' AND issued_on < '2025-05-24'
  AND NOT EXISTS (SELECT 1 FROM edge e JOIN node i ON i.id = e.src
                  WHERE e.dst = node.id AND e.rel = 'INSPECTS' AND i.done_on >= '2025-05-24')
  AND NOT EXISTS (SELECT 1 FROM edge e WHERE e.dst = node.id AND e.rel = 'APPEALS');
