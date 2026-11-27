"""Draws the network diagram for the wiki page."""
import sqlite3
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]


def load(conn):
    g = nx.Graph()
    for name, kind in conn.execute("SELECT name, kind FROM device"):
        g.add_node(name, kind=kind)
    for a, b, gbps in conn.execute("SELECT a, b, gbps FROM link"):
        g.add_edge(a, b, gbps=gbps)
    return g


def main():
    conn = sqlite3.connect(ROOT / "var" / "inventory.db")
    g = load(conn)
    with open(ROOT / "var" / "topology.dot", "w") as f:
        f.write("graph net {\n")
        for a, b, d in g.edges(data=True):
            f.write(f'  "{a}" -- "{b}" [label="{d["gbps"]:g}G"];\n')
        f.write("}\n")


if __name__ == "__main__":
    main()
