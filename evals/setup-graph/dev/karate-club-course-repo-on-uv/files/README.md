# clubnet

Teaching material for the network-analysis module: the karate club friendship network (34 members,
78 ties) and a few questions about it, answered in plain Python.

Requires Python 3.12+ and NetworkX 3.2.

## Ask

    uv run python -m clubnet.cli factions
    uv run python -m clubnet.cli bridges
    uv run python -m clubnet.cli ego 33

The data in `data/` is the published network; treat it as read-only course material.
