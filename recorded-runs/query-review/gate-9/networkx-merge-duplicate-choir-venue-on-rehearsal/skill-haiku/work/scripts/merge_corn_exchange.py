# Rehearsal only: merge the duplicate V-CORNX into V-CORN.
# Walks from V-CORNX move to V-CORN; where both link the same place, the shorter walk is kept.
# The V-CORN to V-CORNX link goes with the node. V-CORN keeps its name and attributes.
DUP, KEEP = "V-CORNX", "V-CORN"
moved, kept_existing, took_shorter, dropped = [], [], [], []
for nbr in list(G.neighbors(DUP)):
    if nbr == KEEP:
        dropped.append(nbr)
        continue
    mins = G.edges[DUP, nbr]["minutes"]
    if G.has_edge(KEEP, nbr):
        if mins < G.edges[KEEP, nbr]["minutes"]:
            G.edges[KEEP, nbr]["minutes"] = mins
            took_shorter.append(nbr)
        else:
            kept_existing.append(nbr)
    else:
        G.add_edge(KEEP, nbr, minutes=mins)
        moved.append(nbr)
G.remove_node(DUP)
print(f"moved {sorted(moved)}; shorter on {KEEP} {sorted(took_shorter)}; kept {KEEP} {sorted(kept_existing)}; dropped {sorted(dropped)}")
