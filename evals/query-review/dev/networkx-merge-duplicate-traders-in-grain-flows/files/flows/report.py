"""Weekly market report: top buyers and each seller's share of its sales per buyer."""


def seller_shares(G, seller):
    out = sum(d["tonnes"] for _, _, d in G.out_edges(seller, data=True))
    return {v: d["tonnes"] / out for _, v, d in G.out_edges(seller, data=True)} if out else {}


def top_buyers(G, n=10):
    return sorted(G.nodes, key=lambda v: -sum(d["tonnes"] for _, _, d in G.in_edges(v, data=True)))[:n]
