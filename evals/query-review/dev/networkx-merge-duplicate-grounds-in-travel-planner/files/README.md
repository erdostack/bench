# away-travel

Travel planner for the regional amateur league: which road legs a team drives to reach an away ground.
Grounds are nodes, legs are edges of an undirected NetworkX `Graph` with `km` and `origin`.

- `travel/graph.py`: `load_graph()` reads `data/grounds.json`. `travel/merge.py`: duplicate grounds.
- `travel/plan.py`: the planner. `docs/travel.md`: the data.
- `python -m pytest tests` runs the tests (NetworkX 3.7).
