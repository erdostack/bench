"""Batch lead time. Untimed steps count 20 minutes."""


def lead_time(conn, recipe_id):
    (total,) = conn.execute("SELECT SUM(COALESCE(minutes, 20)) FROM step WHERE recipe_id = ?", (recipe_id,)).fetchone()
    return total
