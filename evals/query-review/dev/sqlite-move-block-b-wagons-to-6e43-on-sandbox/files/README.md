# trainsheet

Freight train formations as a graph in SQLite (`db/schema.sql`, `docs/model.md`): which wagons and which
locomotive each train has, used for the brake-force and route-availability reports.

- `bin/ts <target> "<sql>"` / `bin/ts <target> --file <file.sql>`: run SQL on a target in `config/targets.toml`.
- `bin/brake-report <db> <train ref>`: brake-force percentage for a train.
- `changes/`: reviewed changes for `tops` only.
- `docs/TARGETS.md`: what each target is.
