"""Archive leaf categories that have no live products."""
from catalog.tree import subtree_ids

ROOT = 1


def run(conn):
    archived = 0
    ids = subtree_ids(conn, ROOT)
    for start in range(0, len(ids), 500):
        chunk = ids[start:start + 500]
        marks = ",".join("?" * len(chunk))
        with conn:
            archived += conn.execute(
                f"""UPDATE categories SET archived = 1
                    WHERE id IN ({marks}) AND archived = 0
                      AND NOT EXISTS (SELECT 1 FROM categories c WHERE c.parent_id = categories.id)
                      AND NOT EXISTS (SELECT 1 FROM products p WHERE p.category_id = categories.id AND p.archived = 0)""",
                chunk).rowcount
    return archived
