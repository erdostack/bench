"""Rolled-up unit cost. Finance's rule (docs/graph/DECISION.md): anything missing below an assembly means no cost."""


def rolled_cost(conn, item_id):
    items = {i: (k, s, l) for i, k, s, l in conn.execute("SELECT id, kind, std_cost, labour_cost FROM item")}
    lines = {}
    for p, c, q in conn.execute("SELECT parent_id, component_id, qty FROM bom_line"):
        lines.setdefault(p, []).append((c, q))
    memo = {}

    def cost(i, path=()):
        if i not in items:
            raise ValueError(f"no item with id {i}")
        if i in memo:
            return memo[i]
        kind, std, labour = items[i]
        if kind == "bought":
            total = std
        else:
            total = labour or 0.0
            for c, q in lines.get(i, []):
                total += q * cost(c, path + (i,))
        memo[i] = total
        return total

    return cost(item_id)
