from graphio import load, save

G = load()
seen, drop = set(), []
for u, v, k, d in sorted(G.edges(keys=True, data=True), key=lambda e: e[2]):
    sig = (u, v, d["object"])
    if sig in seen:
        drop.append((u, v, k))
    else:
        seen.add(sig)
G.remove_edges_from(drop)
save(G)
print(len(drop))
