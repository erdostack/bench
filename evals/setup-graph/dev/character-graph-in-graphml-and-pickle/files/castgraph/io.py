"""Load the character graph: from the pickle cache when it is fresh, otherwise from GraphML."""
import pickle
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parent.parent
GRAPHML = ROOT / "data" / "lesmis.graphml"
CACHE = ROOT / "cache" / "lesmis.pickle"


def load() -> nx.Graph:
    if CACHE.exists() and CACHE.stat().st_mtime >= GRAPHML.stat().st_mtime:
        with CACHE.open("rb") as handle:
            return pickle.load(handle)
    graph = nx.read_graphml(GRAPHML)
    CACHE.parent.mkdir(exist_ok=True)
    with CACHE.open("wb") as handle:
        pickle.dump(graph, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return graph
