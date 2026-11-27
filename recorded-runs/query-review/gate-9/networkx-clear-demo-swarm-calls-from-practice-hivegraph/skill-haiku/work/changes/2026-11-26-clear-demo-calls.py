"""Clear the DEMO- session calls left from last night's training session, with their links.
Removes only report nodes whose code starts with DEMO- and every edge touching them. Trainee accounts (T-),
the AR-DEMO area, the seed members and areas, and the standard EX- exercises stay."""


def run(G):
    demo = [n for n, d in G.nodes(data=True)
            if d.get("kind") == "report" and str(d.get("code", n)).startswith("DEMO-")]
    edges = {frozenset((u, v)) for u, v in G.edges() if u in demo or v in demo}
    G.remove_nodes_from(demo)
    return f"removed {len(demo)} DEMO- calls and {len(edges)} links"
