from catalog.tree import subtree_ids

ROOT = 7


def run(conn):
    ids = subtree_ids(conn, ROOT)
    counts = {"categories": 0, "products": 0}
    for start in range(0, len(ids), 50):
        chunk = ids[start:start + 50]
        marks = ",".join("?" * len(chunk))
        with conn:
            counts["products"] += conn.execute(f"UPDATE products SET archived = 1 WHERE category_id IN ({marks})", chunk).rowcount
            counts["categories"] += conn.execute(f"UPDATE categories SET archived = 1 WHERE id IN ({marks})", chunk).rowcount
    return counts
