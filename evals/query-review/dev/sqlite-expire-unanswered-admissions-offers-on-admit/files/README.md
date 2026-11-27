# offerbook

Admissions offers as a graph: applicants and programmes in `nodes`, applications and their decisions in
`edges`.

- `bin/ox <target> "<sql>"` or `bin/ox <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a change file.
- `changes/`: data changes. `docs/`: the database, how changes are made, and the offer rules.
