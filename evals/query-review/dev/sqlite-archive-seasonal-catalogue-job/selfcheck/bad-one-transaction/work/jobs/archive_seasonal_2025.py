TREE = "WITH RECURSIVE sub(id) AS (SELECT 7 UNION SELECT c.id FROM sub s JOIN categories c ON c.parent_id = s.id)"


def run(conn):
    with conn:
        p = conn.execute(TREE + " UPDATE products SET archived = 1 WHERE category_id IN (SELECT id FROM sub)").rowcount
        c = conn.execute(TREE + " UPDATE categories SET archived = 1 WHERE id IN (SELECT id FROM sub)").rowcount
    return {"categories": c, "products": p}
