"""Practice run: C-14's departures 2026-12-01..2026-12-12 move to C-22 (MOT)."""


def change(G):
    moved = 0
    for dp, coach, d in list(G.edges(data=True)):
        if d.get("kind") == "run_by" and coach == "C-14":
            G.remove_edge(dp, coach)
            G.add_edge(dp, "C-22", **d)
            moved += 1
    return moved
