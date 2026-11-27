# shuttle

Bus routes for the Fernhill Learning Trust's nine schools as a graph in SQLite (`nodes`, `edges`).

- `bin/tq <target> "<sql>"` or `bin/tq <target> --file <file.sql>`: run SQL on a target in `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (for `live`).
- `scripts/make_trial.py`: builds `data/trial.sqlite` from scratch.
- `docs/targets.md`: the targets. `docs/model.md`: the graph.
