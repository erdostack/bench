"""One-off: archive the "Seasonal 2025" tree (category 7), its categories at any depth and their products."""

ROOT = 7
CHUNK = 1000

# catalog.tree.subtree_ids stops at 2,000 categories (it is the menu's helper); this tree has about 4,500,
# so the walk is done here without a limit. The tree has no loops (one parent per category).
TREE = """
WITH RECURSIVE sub(id) AS (
    SELECT ?
    UNION
    SELECT c.id FROM sub s JOIN categories c ON c.parent_id = s.id
)
SELECT id FROM sub ORDER BY id
"""


def run(conn):
    ids = [r[0] for r in conn.execute(TREE, (ROOT,))]
    counts = {"categories": 0, "products": 0}
    for start in range(0, len(ids), 200):
        chunk = ids[start:start + 200]
        marks = ",".join("?" * len(chunk))
        while True:      # products of these categories, at most CHUNK per transaction
            with conn:
                n = conn.execute(f"UPDATE products SET archived = 1 WHERE id IN (SELECT id FROM products "
                                 f"WHERE category_id IN ({marks}) AND archived = 0 LIMIT {CHUNK})", chunk).rowcount
            counts["products"] += n
            if n < CHUNK:
                break
        with conn:
            counts["categories"] += conn.execute(f"UPDATE categories SET archived = 1 WHERE id IN ({marks}) AND archived = 0",
                                                 chunk).rowcount
    return counts
