"""Rolled-up cost, in Python. Missing component anywhere below: "incomplete" (finance's rule)."""
from functools import lru_cache


def rolled_cost(conn, item_id):
    items = {i: (k, s, l) for i, k, s, l in conn.execute("SELECT id, kind, std_cost, labour_cost FROM item")}
    lines = {}
    for p, c, q in conn.execute("SELECT parent_id, component_id, qty FROM bom_line"):
        lines.setdefault(p, []).append((c, q))

    @lru_cache(maxsize=None)
    def cost(i):
        if i not in items:
            return None
        kind, std, labour = items[i]
        if kind == "bought":
            return std
        total = labour or 0.0
        for c, q in lines.get(i, []):
            sub = cost(c)
            if sub is None:
                return None
            total += q * sub
        return total

    result = cost(item_id)
    return "incomplete" if result is None else result
