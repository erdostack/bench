"""Reviewed (planners, PLN-88): C-09 is in the paint shop 2026-11-09 to 2026-11-11; its departures move to C-03."""


def change(G):
    moved = 0
    for dp, coach, d in list(G.edges(data=True)):
        if d.get("kind") == "run_by" and coach == "C-09" and "2026-11-09" <= G.nodes[dp]["departs_on"] <= "2026-11-11":
            G.remove_edge(dp, coach)
            G.add_edge(dp, "C-03", **d)
            moved += 1
    return moved
