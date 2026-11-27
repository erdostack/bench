# cantata

Scheduling for the Harrowgate Choral Festival (1 to 21 March 2027) as a graph in SQLite: venues, choirs and
the performance slots that join them.

- `bin/fq <target> "<sql>"` or `bin/fq <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a data change (see `docs/targets.md`).
- `changes/`: data changes, one `.sql` file each. `queries/`: saved queries the timetable uses.
- `db/schema.sql`: the schema. `docs/`: targets and the model.
