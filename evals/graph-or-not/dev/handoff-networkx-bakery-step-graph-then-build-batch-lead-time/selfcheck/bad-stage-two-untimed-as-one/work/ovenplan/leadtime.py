"""Batch lead time with networkx's longest path."""
import networkx as nx


def lead_time(conn, recipe_id):
    g = nx.DiGraph()
    minutes = dict(conn.execute("SELECT id, minutes FROM step WHERE recipe_id = ?", (recipe_id,)).fetchall())
    g.add_node("start")
    g.add_nodes_from(minutes)
    for before, after in conn.execute("SELECT before_id, after_id FROM step_dep"):
        if before in minutes:
            g.add_edge(before, after)
    for s in minutes:
        if g.in_degree(s) == 0:
            g.add_edge("start", s)
    g.add_node("end")
    for s in minutes:
        if g.out_degree(s) == 0:
            g.add_edge(s, "end")
    for u, v in g.edges:
        if v in minutes and minutes[v] is not None:
            g.edges[u, v]["w"] = minutes[v]
    return nx.dag_longest_path_length(g, weight="w")
