import networkx as nx


def assign(conn):
    rows = conn.execute(
        "SELECT p.id, j.id FROM project p JOIN judge_category c ON c.category = p.category "
        "JOIN judge j ON j.id = c.judge_id WHERE j.school <> p.school").fetchall()
    g = nx.Graph()
    g.add_edges_from((("p", p), ("j", j)) for p, j in rows)
    tops = [n for n in g if n[0] == "p"]
    m = nx.bipartite.hopcroft_karp_matching(g, top_nodes=tops)
    return {a[1]: b[1] for a, b in m.items() if a[0] == "p"}
