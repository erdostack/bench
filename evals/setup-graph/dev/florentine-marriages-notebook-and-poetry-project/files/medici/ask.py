"""python -m medici.ask brokers | path FROM TO | degree"""
import sys

import networkx as nx

from medici.graph import marriages


def main(argv: list[str]) -> None:
    graph = marriages()
    what = argv[0] if argv else "brokers"
    if what == "brokers":
        for family, score in sorted(nx.betweenness_centrality(graph).items(), key=lambda kv: -kv[1])[:5]:
            print(f"{family}\t{score:.3f}")
    elif what == "path":
        print(" -> ".join(nx.shortest_path(graph, argv[1], argv[2])))
    elif what == "degree":
        for family, n in sorted(graph.degree, key=lambda kv: -kv[1]):
            print(f"{family}\t{n}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
