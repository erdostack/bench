"""python -m curio.similarity.build --out <file>: export the maker graph and score similar makers with NetworkX.

Runs once a week from cron. It reads the maker subgraph out of the database, builds an in-memory graph and
writes a JSON file that the website serves statically. Nothing is written back to the database.
"""
import argparse
import json

import networkx as nx

from .. import graph

EDGES = "MATCH (a:Maker)-[:TRAINED_UNDER]-(b:Maker) WHERE a.name < b.name RETURN a.name AS a, b.name AS b"


def build() -> nx.Graph:
    g = nx.Graph()
    g.add_edges_from((row["a"], row["b"]) for row in graph.read(EDGES))
    return g


def similar(g: nx.Graph, top: int = 5) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for maker in g:
        scores = nx.jaccard_coefficient(g, ((maker, other) for other in g if other != maker))
        ranked = sorted(scores, key=lambda item: -item[2])[:top]
        out[maker] = [other for _, other, score in ranked if score > 0]
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(similar(build()), handle, indent=2, sort_keys=True)


if __name__ == "__main__":
    main()
