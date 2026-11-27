# netinv

Network inventory service: devices (OLTs, aggregation switches, ONTs) and the links between their ports.
The device picker in `ui/` reads the `devices` table.

- `bin/inv <target> "<sql>"`: run SQL on a target in `config/targets.toml`.
- `bin/seed`: rebuild the developer database from `db/schema.sql` and generated data.
- `changes/`: data changes for production, `NNNN_<what>.sql`, reviewed in a PR.
- `docs/ENVIRONMENTS.md`: where each target points.
