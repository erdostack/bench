# climnet

The automatic weather station network as a graph in SQLite: stations, the telemetry hubs that poll them and
the sensors installed at them in `nodes`, the links in `edges`. The hub poller in `poller/` reads it.

- `bin/cn <target> "<sql>"` or `bin/cn <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `python3 scripts/build_scratch.py`: (re)build your scratch database, `var/scratch.db`, from a fixed seed.
- `changes/`: reviewed data changes for `network` (see `docs/targets.md`).
- `docs/`: targets and the station model.
