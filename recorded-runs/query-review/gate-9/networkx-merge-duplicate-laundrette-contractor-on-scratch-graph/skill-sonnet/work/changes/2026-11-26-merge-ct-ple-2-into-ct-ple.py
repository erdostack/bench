"""Planning experiment: CT-PLE-2 is the same firm as CT-PLE (typed in twice from the contract PDFs); merge it
into CT-PLE. Its machines' serviced_by links move to CT-PLE with their contract and since kept; its based_at
link duplicates CT-PLE's (both Halifax depot) and goes with the node. Returns the number of links moved."""
KEEP, DROP = "CT-PLE", "CT-PLE-2"


def run(G):
    if DROP not in G:
        return 0
    moved = 0
    for m, c, d in list(G.in_edges(DROP, data=True)):
        if d.get("kind") == "serviced_by":
            G.remove_edge(m, c)
            G.add_edge(m, KEEP, **d)
            moved += 1
    G.remove_node(DROP)
    return moved
