# heatgrid

The district heating network as a graph: plants, pipe sections, building substations, buildings and heat
meters are rows in `nodes`, and how they connect are rows in `edges` (`docs/model.md`). The network tracer,
the outage planner and the customer portal read it.

- `bin/hq <target> "<sql>"` (or `--file <file.sql>`): run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, one file each, `NNNN_<what>.py`.
- `docs/TARGETS.md`: what each target is and how data changes reach it.

This checkout lives on the ops jump host, where `mnt/` holds the database volumes.
