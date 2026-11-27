"""python -m clubnet.cli <factions|bridges|ego N>"""
import sys

import networkx as nx
from networkx.algorithms import community

from clubnet.load import club_graph


def main(argv: list[str]) -> None:
    graph = club_graph()
    if not argv or argv[0] == "factions":
        for n, group in enumerate(community.greedy_modularity_communities(graph, weight="weight")):
            print(n, sorted(group))
    elif argv[0] == "bridges":
        for a, b in sorted(nx.bridges(graph)):
            print(a, b)
    elif argv[0] == "ego":
        ego = nx.ego_graph(graph, int(argv[1]))
        print(ego.number_of_nodes(), "members,", ego.number_of_edges(), "ties")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
