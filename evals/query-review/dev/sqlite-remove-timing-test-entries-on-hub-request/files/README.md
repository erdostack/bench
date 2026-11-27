# harriers-results

Race results for the running club: athletes and races are nodes, a `results` row is an edge (athlete
finished race). The club website, the club championship table and the age-grading emails read it.

- `bin/rr <target> "<sql>"`: run SQL on a target from `config/targets.toml`.
- `bin/rr-apply <target> changes/<file>.py`: apply a change file (calls its `apply(conn)`).
- `changes/`: data changes, `NNN-<slug>.py`, one per change.
- `docs/ENVIRONMENTS.md`, `docs/bibs.md`, `db/schema.sql`.
