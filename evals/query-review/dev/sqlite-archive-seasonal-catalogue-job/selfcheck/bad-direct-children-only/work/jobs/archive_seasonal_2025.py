def run(conn):
    ids = [7] + [r[0] for r in conn.execute("SELECT id FROM categories WHERE parent_id = 7")]
    marks = ",".join("?" * len(ids))
    counts = {"categories": 0, "products": 0}
    while True:
        with conn:
            n = conn.execute(f"UPDATE products SET archived = 1 WHERE id IN (SELECT id FROM products WHERE category_id IN ({marks}) "
                             f"AND archived = 0 LIMIT 1000)", ids).rowcount
        counts["products"] += n
        if not n:
            break
    with conn:
        counts["categories"] = conn.execute(f"UPDATE categories SET archived = 1 WHERE id IN ({marks})", ids).rowcount
    return counts
