# tote-router

Routes totes through the parcel hub's conveyor network, from an induction point to a chute.

- `data/conveyors.json`: belt segments. `docs/plant.md`: what the fields mean.
- `sorter/routing.py`: `load_conveyors()` and `route(G, src, dst)` (list of nodes, or None if the tote can't get there).
