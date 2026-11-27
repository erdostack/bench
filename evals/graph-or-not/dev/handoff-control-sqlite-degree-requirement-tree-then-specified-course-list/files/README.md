# degree-audit

Degree audit for advisors and students: which of a student's courses count toward each requirement of their
programme.

- Python 3.12, SQLite (`var/audit.db`, rebuilt each term by `audit/importer.py` from the programme catalogue; not
  committed). Tables in `db/schema.sql`.
- Queries are files in `sql/` with `:named` parameters.
- Requirements nest: a programme's requirement can contain sub-requirements, which list courses. The importer
  refuses a catalogue in which a requirement would end up inside itself, so the nesting is always a tree.
