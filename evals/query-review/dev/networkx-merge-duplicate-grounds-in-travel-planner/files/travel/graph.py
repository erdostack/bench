import json
from pathlib import Path

import networkx as nx

DATA = Path(__file__).resolve().parent.parent / "data"


def load_graph(path=DATA / "grounds.json") -> nx.Graph:
    return nx.node_link_graph(json.loads(Path(path).read_text()), edges="links")


def load_merges(path=DATA / "ground_merges.csv") -> list[tuple[str, str]]:
    lines = Path(path).read_text().splitlines()[1:]
    return [tuple(line.split(",")) for line in lines if line.strip()]
