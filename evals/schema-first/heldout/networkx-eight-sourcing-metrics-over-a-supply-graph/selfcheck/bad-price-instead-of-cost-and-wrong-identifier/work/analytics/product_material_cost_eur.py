def _edges(G, label):
    """(source, target, attributes) of every edge with this label."""
    return [(u, v, d) for u, v, d in G.edges(data=True) if d.get("label") == label]


def compute(G):
    price = {}
    for _sup, part, d in _edges(G, "supplies"):
        price[part] = min(price.get(part, 1e18), d["price_eur"])
    cost = {}
    for part, product, d in _edges(G, "component_of"):
        sku = G.nodes[product]["sku"]
        cost[sku] = cost.get(sku, 0.0) + d["qty"] * price.get(part, 0)
    return cost
