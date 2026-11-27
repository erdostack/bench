"""012: the importer created tag:chess-club next to tag:chess. Move its hasInterest edges to tag:chess and drop it.
Reviewed: o.lindahl. Applied to live 2026-10-27."""


def run(G):
    moved = 0
    for u in list(G.predecessors("tag:chess-club")):
        G.add_edge(u, "tag:chess", kind="hasInterest")
        moved += 1
    G.remove_node("tag:chess-club")
    return moved
