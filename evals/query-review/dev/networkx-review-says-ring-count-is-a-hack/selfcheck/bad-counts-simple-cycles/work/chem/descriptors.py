"""Graph descriptors over molecule graphs (docs/descriptors.md)."""
import networkx as nx


def to_graph(mol):
    G = nx.Graph()
    G.add_nodes_from(range(len(mol["atoms"])))
    G.add_edges_from((a, b) for a, b, _order in mol["bonds"])
    return G


def ring_count(mol):
    G = to_graph(mol)
    return len(list(nx.simple_cycles(G)))


def heavy_atoms(mol):
    return sum(1 for a in mol["atoms"] if a != "H")
