"""Nightly: load the freshly extracted graph, apply clean-ups, save it for the dashboard."""
import sys
from pathlib import Path

from tools.graphio import load, save

GRAPH = Path(__file__).resolve().parent.parent / "graph" / "targets.json"


def main():
    G = load(GRAPH)
    try:
        from tools.prune_legacy import prune
    except ImportError:
        prune = None
    if prune is not None:
        removed = prune(G)
        print(f"pruned {len(removed)} legacy targets", file=sys.stderr)
    save(G, GRAPH)


if __name__ == "__main__":
    main()
