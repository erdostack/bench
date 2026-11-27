import networkx as nx


def close_groups(conn):
    g = nx.Graph()
    by_event = {}
    for person, event in conn.execute("SELECT person, event FROM attendance"):
        by_event.setdefault(event, []).append(person)
    for people in by_event.values():
        for i, a in enumerate(people):
            for b in people[i + 1:]:
                g.add_edge(a, b)
    return sorted(sorted(c) for c in nx.connected_components(g))
