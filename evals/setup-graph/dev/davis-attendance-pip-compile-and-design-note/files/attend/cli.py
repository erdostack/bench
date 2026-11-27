import sys

import networkx as nx
from networkx.algorithms import bipartite

from attend.graph import attendance


def main(argv: list[str]) -> None:
    graph = attendance()
    side = {n for n, b in graph.nodes(data="bipartite") if b == (0 if argv[1:2] != ["events"] else 1)}
    if argv[:1] == ["project"]:
        projected = bipartite.weighted_projected_graph(graph, side)
        for a, b, w in sorted(projected.edges(data="weight"), key=lambda e: -e[2])[:15]:
            print(f"{a}\t{b}\t{w}")
    elif argv[:1] == ["cores"]:
        projected = bipartite.weighted_projected_graph(graph, side)
        for node, k in sorted(nx.core_number(projected).items(), key=lambda kv: -kv[1]):
            print(f"{node}\t{k}")
    else:
        sys.exit("usage: scripts/run.sh project <women|events> | cores")


if __name__ == "__main__":
    main(sys.argv[1:])
