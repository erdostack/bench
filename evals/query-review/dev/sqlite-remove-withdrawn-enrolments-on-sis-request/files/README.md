# sisgraph

The registry's enrolment graph: students, course sections and the enrolments between them, in SQLite
node and edge tables, plus the term calendar.

- `bin/sisq <target> "<sql>"` or `bin/sisq <target> --file <file.sql>`: run SQL on a target from
  `config/targets.toml`.
- `bin/apply <target> datafix/<file>.py`: apply a data fix.
- `datafix/`: data fixes, one file each. See `docs/datafix.md`.
- `docs/enrolment.md`: what an enrolment is and what its statuses mean.
