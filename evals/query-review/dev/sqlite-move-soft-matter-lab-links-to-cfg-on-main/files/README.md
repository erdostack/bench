# researchgraph

The faculty's research graph: people, research groups, departments and papers, and who belongs to and
publishes with which group. SQLite, as node and edge tables. The research portal and the REF export
read it.

- `bin/rgq <target> "<sql>"` or `bin/rgq <target> --file <file.sql>`: run SQL on a target from
  `config/targets.toml`.
- `bin/migrate <target> changes/<file>.py`: apply a change file.
- `changes/`: changes to the data, one file each. How to write one: `docs/changes.md`.
- `docs/model.md`: node kinds and edge types.
