WITH RECURSIVE
  nb(a, b) AS (SELECT x.segment_id, y.segment_id FROM segment x JOIN segment y
               ON y.segment_id <> x.segment_id AND (y.j1 IN (x.j1, x.j2) OR y.j2 IN (x.j1, x.j2))),
  walk(seg, d) AS (SELECT :segment_id, 0
                   UNION SELECT nb.b, walk.d + 1 FROM walk JOIN nb ON nb.a = walk.seg WHERE walk.d < :hops)
SELECT seg AS segment_id FROM walk WHERE seg <> :segment_id GROUP BY seg;
