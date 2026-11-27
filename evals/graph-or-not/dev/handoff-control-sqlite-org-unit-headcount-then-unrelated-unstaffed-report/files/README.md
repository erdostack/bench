# unitbook

The organisation's units (directorates, departments, teams) and who is assigned where, for the HR reporting
pack. One SQLite database (`var/unitbook.db`, schema in `db/schema.sql`), refreshed from the HR system nightly.

- `reports/*.sql`: the reporting pack's queries; run one with `python -m orgunits.run reports/<name>.sql key=value ...`.
- `orgunits/run.py`: the runner.

Python 3.11+, standard library only.
