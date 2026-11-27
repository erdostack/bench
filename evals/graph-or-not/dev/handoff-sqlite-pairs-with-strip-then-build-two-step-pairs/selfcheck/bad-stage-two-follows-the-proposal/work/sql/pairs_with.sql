WITH RECURSIVE nb (p, q) AS (
    SELECT product_a, product_b FROM pairing UNION ALL SELECT product_b, product_a FROM pairing
), walk (id, depth) AS (
    SELECT :product_id, 0
    UNION
    SELECT nb.q, walk.depth + 1 FROM walk JOIN nb ON nb.p = walk.id WHERE walk.depth < 3
)
SELECT DISTINCT id AS product_id FROM walk WHERE id <> :product_id;
