"""Planning experiment: CT-PLE-2 (Pennine Laundry Engineering Ltd.) is the same firm as CT-PLE, typed in twice
from the contract PDFs. Move its serviced_by edges to CT-PLE, keeping each contract ref and since date, then
drop CT-PLE-2. Its based_at edge duplicates CT-PLE's (both Halifax), so it is dropped with the node."""


def run(G):
    dup, keep = "CT-PLE-2", "CT-PLE"
    moved = 0
    for m, c, d in list(G.in_edges(dup, data=True)):
        if d.get("kind") != "serviced_by":
            continue
        if G.has_edge(m, keep):
            raise ValueError(f"{m} is already serviced by {keep}; refusing to merge")
        G.remove_edge(m, dup)
        G.add_edge(m, keep, **d)
        moved += 1
    G.remove_node(dup)
    return moved
