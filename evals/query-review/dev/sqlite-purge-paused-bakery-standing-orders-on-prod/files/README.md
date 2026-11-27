# bakesheet

Millrace Bakery's wholesale graph in SQLite: trade customers, products and van rounds in `nodes`; standing
orders and round membership in `edges` (`docs/model.md`). The overnight bake sheet and the drivers' tablets
read it.

- `bin/bq <target> "<sql>"` (or `--file <file.sql>`): run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a change file (`docs/changes.md`).
- `changes/`: data changes.
