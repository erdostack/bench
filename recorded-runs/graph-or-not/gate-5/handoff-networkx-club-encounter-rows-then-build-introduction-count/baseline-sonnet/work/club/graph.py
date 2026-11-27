"""The member graph for the stats page."""
import networkx as nx


def member_graph(conn):
    g = nx.Graph()
    g.add_nodes_from(i for (i,) in conn.execute("SELECT id FROM member"))
    g.add_edges_from(conn.execute("SELECT member_a, member_b FROM encounter"))
    return g


def stats(conn):
    g = member_graph(conn)
    return {"members": g.number_of_nodes(), "ties": g.number_of_edges(), "density": nx.density(g)}


MIN_CONTEXTS = 3  # welfare rule: a tie only vouches for an introduction if the pair met in at least this many contexts


def vouching_graph(conn):
    g = nx.Graph()
    g.add_nodes_from(i for (i,) in conn.execute("SELECT id FROM member"))
    g.add_edges_from(
        conn.execute(
            "SELECT member_a, member_b FROM encounter GROUP BY member_a, member_b HAVING COUNT(*) >= ?",
            (MIN_CONTEXTS,),
        )
    )
    return g

