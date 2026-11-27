Added impacted_by() in svcmap/impact.py.

One thing had to change first: load_graph() built an undirected nx.Graph, so "who calls X" and "who X calls" were
the same thing, and an ancestors() call on it returned the whole connected map (259 services for any store). I made
load_graph() return a DiGraph (caller -> callee) and updated neighbours() to look both ways so the map's side
panel is unchanged. impacted_by() is nx.ancestors on that graph; the few callback loops in the traces are fine
for it. audit-store-012 now lists 63 services. Tests pass.
