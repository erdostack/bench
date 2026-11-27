WITH RECURSIVE tree(root, id, depth) AS (
  SELECT id, id, 0 FROM account
  UNION ALL
  SELECT t.root, a.id, t.depth + 1 FROM tree t JOIN account a ON a.parent_id = t.id
)
SELECT a.id AS account_id,
       (SELECT coalesce(sum(p.amount_cents), 0)
          FROM tree t JOIN posting p ON p.account_id = t.id
         WHERE t.root = a.id AND p.posted_on >= :period || '-01' AND p.posted_on < date(:period || '-01', '+1 month')) AS total
FROM account a;
