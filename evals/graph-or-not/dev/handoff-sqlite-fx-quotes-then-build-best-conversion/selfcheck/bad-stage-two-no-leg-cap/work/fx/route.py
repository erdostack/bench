"""Currency conversion for checkout. conn is a sqlite3 connection to the pod's quotes cache."""


def direct_rate(conn, base, quote):
    """Best rate any provider quotes for base -> quote, or None if the pair is not quoted."""
    row = conn.execute("SELECT max(rate) FROM quote WHERE base = ? AND quote = ?", (base, quote)).fetchone()
    return row[0]


def convert(conn, amount, base, quote):
    rate = direct_rate(conn, base, quote)
    if rate is None:
        # TODO: most pairs aren't quoted directly; route through other currencies.
        raise LookupError(f"no quote for {base}->{quote}")
    return amount * rate
import math

import networkx as nx


def best_route(conn, src, dst):
    """Best rate src -> dst: shortest path on -log(rate), restricted currencies excluded."""
    restricted = {r[0] for r in conn.execute("SELECT code FROM restricted_currency")}
    g = nx.DiGraph()
    for base, quote, rate in conn.execute("SELECT base, quote, max(rate) FROM quote GROUP BY base, quote"):
        if (base in restricted and base != src) or (quote in restricted and quote != dst):
            continue
        g.add_edge(base, quote, w=-math.log(rate), rate=rate)
    try:
        path = nx.bellman_ford_path(g, src, dst, weight="w")
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None
    return math.prod(g[a][b]["rate"] for a, b in zip(path, path[1:])), path
