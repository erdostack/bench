"""Load the membership export into networkx. conn is a sqlite3 connection to var/consortium.db."""
import networkx as nx


def load_graph(conn):
    """Bipartite graph: organisation ids (int) and working-group codes (str) as nodes, one edge per membership,
    with the membership's role and its attendance as `weight`."""
    g = nx.Graph()
    for org_id, name in conn.execute("SELECT id, name FROM organisation"):
        g.add_node(org_id, kind="org", name=name)
    for code, name in conn.execute("SELECT code, name FROM working_group"):
        g.add_node(code, kind="group", name=name)
    for org_id, code, role, meetings in conn.execute(
            "SELECT org_id, group_code, role, meetings_per_year FROM membership"):
        g.add_edge(org_id, code, role=role, weight=meetings)
    return g


def groups_of(g, org_id):
    return sorted(n for n in g.neighbors(org_id))


def liaison_chain(g, from_org, to_org):
    """Shortest chain of introductions between two organisations: [org, group, org, group, ..., org].

    Observer seats do not count: an org neither introduces nor is introduced through a group it only
    observes. "Shortest" is fewest introductions, so the attendance `weight` is deliberately ignored
    (no weight= argument). Equally short chains: any one is returned.
    Returns None if there is no chain, and raises KeyError if either id is not an organisation.
    """
    for org_id in (from_org, to_org):
        if g.nodes.get(org_id, {}).get("kind") != "org":
            raise KeyError(org_id)
    seated = nx.subgraph_view(g, filter_edge=lambda u, v: g[u][v]["role"] != "observer")
    try:
        return nx.shortest_path(seated, from_org, to_org)
    except nx.NetworkXNoPath:
        return None
