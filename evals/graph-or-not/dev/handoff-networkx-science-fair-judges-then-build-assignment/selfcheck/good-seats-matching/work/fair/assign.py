import networkx as nx

LIMIT = 3


def assign(conn):
    rows = conn.execute(
        "SELECT p.id, j.id FROM project p JOIN judge_category c ON c.category = p.category "
        "JOIN judge j ON j.id = c.judge_id WHERE j.school <> p.school").fetchall()
    judges = {j for _, j in rows}
    g = nx.Graph()
    projects = {p for p, _ in rows}
    g.add_nodes_from(("p", p) for p in projects)
    for p, j in rows:
        for seat in range(LIMIT):            # each judge has three seats
            g.add_edge(("p", p), ("j", j, seat))
    m = nx.bipartite.hopcroft_karp_matching(g, top_nodes=[("p", p) for p in projects])
    return {a[1]: b[1] for a, b in m.items() if a[0] == "p"}
