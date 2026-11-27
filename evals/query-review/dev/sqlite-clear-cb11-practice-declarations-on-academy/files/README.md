# customs-academy

The broker-training system: trainee customs brokers lodge practice import declarations against a copy of
real (anonymised) declarations, in an SQLite graph (`db/schema.sql`, `docs/model.md`).

- `bin/cb <target> "<sql>"` / `bin/cb <target> --file <file.sql>`: run SQL on a target in `config/targets.toml`.
- `docs/TARGETS.md`: what each target is.
