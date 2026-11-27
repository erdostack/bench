# arbor-graph

Ashworth Borough Council's street tree inventory as a graph in SQLite: trees, streets and surveyors in
`nodes`, what links them in `edges` (`docs/model.md`). The tree officers' tablets and the public tree map
read it.

- `bin/tq <target> "<sql>"` (or `--file <file.sql>`): run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a change file (`docs/changes.md`).
- `changes/`: data changes. `docs/targets.md`: what each target is.
