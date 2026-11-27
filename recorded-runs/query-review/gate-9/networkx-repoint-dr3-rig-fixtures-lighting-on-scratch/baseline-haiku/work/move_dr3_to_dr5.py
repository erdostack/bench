"""Re-patch the scratch copy: every fixture fed by DR-3 is moved to DR-5, circuit numbers kept."""


def run(G):
    moved = []
    for u, v, d in list(G.in_edges("DR-3", data=True)):
        if d.get("kind") == "fed_by":
            attrs = dict(d)
            G.remove_edge(u, v)
            G.add_edge(u, "DR-5", **attrs)
            moved.append((u, attrs.get("circuit")))
    return f"moved {len(moved)} fixtures from DR-3 to DR-5: " + ", ".join(f"{f}(c{c})" for f, c in moved)
