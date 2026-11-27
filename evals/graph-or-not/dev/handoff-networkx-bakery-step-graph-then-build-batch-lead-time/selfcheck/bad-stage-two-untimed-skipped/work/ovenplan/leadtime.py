"""Batch lead time: the longest chain of steps. """
import networkx as nx

UNTIMED_MINUTES = 20


def lead_time(conn, recipe_id):
    g = nx.DiGraph()
    for step_id, minutes in conn.execute("SELECT id, minutes FROM step WHERE recipe_id = ?", (recipe_id,)):
        g.add_node(step_id, minutes=minutes or 0)
    for before, after in conn.execute(
            "SELECT d.before_id, d.after_id FROM step_dep d JOIN step s ON s.id = d.after_id WHERE s.recipe_id = ?",
            (recipe_id,)):
        g.add_edge(before, after)
    finish = {}
    for node in nx.topological_sort(g):
        start = max((finish[p] for p in g.predecessors(node)), default=0)
        finish[node] = start + g.nodes[node]["minutes"]
    return max(finish.values(), default=0)
