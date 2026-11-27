"""Reading the controller's topology file."""
import networkx as nx


def load(path):
    """The topology as a DiGraph keyed by relay id (int); edge attribute latency_us (int)."""
    return nx.read_graphml(path, node_type=int)


def sites(g):
    return sorted({data.get("site") for _, data in g.nodes(data=True)})
