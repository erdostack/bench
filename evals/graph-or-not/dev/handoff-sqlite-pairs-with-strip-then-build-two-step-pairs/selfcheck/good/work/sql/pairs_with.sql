-- "Pairs with" strip: products one or two pairings away (merch's limit), never the product itself.
WITH nb (p, q) AS (
    SELECT product_a, product_b FROM pairing
    UNION ALL
    SELECT product_b, product_a FROM pairing
),
one AS (SELECT q AS id FROM nb WHERE p = :product_id),
two AS (SELECT nb.q AS id FROM nb JOIN one ON nb.p = one.id)
SELECT id AS product_id FROM one
UNION
SELECT id FROM two WHERE id <> :product_id;
