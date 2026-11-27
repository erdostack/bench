"""Nightly: build the similarity graph from co-listening counts and save it for the shelf service."""
import json
import sys
from pathlib import Path

import networkx as nx

from recs.build import build_graph
from recs.prune import prune_weak


def main(counts_path, out_path):
    G = build_graph(counts_path)
    dropped = prune_weak(G)
    Path(out_path).write_text(json.dumps(nx.node_link_data(G, edges="links")))
    print(f"{G.number_of_nodes()} playlists, {G.number_of_edges()} links, {dropped} pruned")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
