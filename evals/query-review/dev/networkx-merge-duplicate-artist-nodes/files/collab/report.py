"""Collaborator report: python3 -m collab.report"""
import networkx as nx

from collab.graph import load


def top_collaborators(G: nx.Graph, n: int = 20):
    return sorted(((G.degree(a), a, G.nodes[a]["name"]) for a in G), reverse=True)[:n]


def strongest_partnerships(G: nx.Graph, n: int = 20):
    return sorted(((d["releases"], u, v) for u, v, d in G.edges(data=True)), reverse=True)[:n]


if __name__ == "__main__":
    G = load()
    for deg, a, name in top_collaborators(G):
        print(f"{deg:4d}  {a}  {name}")
