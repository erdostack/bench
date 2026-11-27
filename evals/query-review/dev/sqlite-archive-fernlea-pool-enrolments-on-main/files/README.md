# swimgraph

Ashby Vale Council's swimming lessons as a graph in SQLite: pools (sites), lessons, members and teachers
in `nodes`, and enrolments, waitlists and the rest in `edges`. The lessons booking site, the poolside
registers and the teachers' app use it.

- `bin/sg <target> "<sql>"` or `bin/sg <target> --file <file.sql>`: run SQL on a target in `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a data change (calls its `run(conn)`).
- `scripts/rebuild_sandbox.py`: rebuild the sandbox from main.
- `docs/targets.md`: targets and data changes. `docs/model.md`: the model. `docs/archiving.md`: closures.
