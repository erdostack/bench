"""Tests a PR should run: those reaching a changed target through deps edges (tools edges: nightly run only)."""
import networkx as nx


def affected_tests(graph, changed):
    g = nx.DiGraph()
    for name, t in graph["targets"].items():
        g.add_node(name)
        for dep in t["deps"] + t["tools"]:
            g.add_edge(name, dep)
    hit = set()
    for target in changed:
        if target in g:
            hit.add(target)
            hit |= nx.ancestors(g, target)
    return sorted(n for n in hit if graph["targets"][n]["kind"] == "test")
