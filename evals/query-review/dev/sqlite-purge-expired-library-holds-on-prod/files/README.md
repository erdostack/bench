# holdsgraph

Northway Libraries' circulation graph in SQLite: patrons, titles and branches in `nodes`; holds and checkouts
in `edges` (`docs/holds.md`). The circulation desks' holds queue and the patron app read it.

- `bin/lx <target> "<sql>"` (or `--file <file.sql>`): run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a change file (`docs/changes.md`).
- `changes/`: data changes.
