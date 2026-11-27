# bracketbook

Tournament graph for the Emberfall Open circuit: teams, players and tournaments in `nodes`, entries and
rosters in `edges`. The seeding page (`web/seeding.sql`) and the public brackets read it.

- `bin/bq <target> "<sql>"` (or `--file <file.sql>`): run SQL on a target from `targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file.
- `docs/targets.md`: the targets and how changes reach `brackets`.
