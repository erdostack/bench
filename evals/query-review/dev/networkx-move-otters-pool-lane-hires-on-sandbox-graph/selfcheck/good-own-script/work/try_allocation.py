import networkx as nx

G = nx.read_graphml("graphs/sandbox.graphml")
hires = [h for h in G.successors("CLUB-OTTERS") if G.nodes[h].get("kind") == "hire"]
for h in hires:
    for lane in list(G.successors(h)):
        if lane == "POOL-EAST-L3":
            since = G.edges[h, lane]["since"]
            G.remove_edge(h, lane)
            G.add_edge(h, "POOL-EAST-L5", kind="on_lane", since=since)
nx.write_graphml(G, "graphs/sandbox.graphml")
