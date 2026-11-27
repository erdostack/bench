# turnover

Housekeeping tasks for the Larkspur Hotel as a graph in SQLite: rooms, task types and attendants in `nodes`,
scheduled tasks and section assignments in `edges`. The attendants' tablets and the night audit read it.

- `bin/hkq <target> "<sql>"` or `bin/hkq <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, one file each.
- `importer/`: the nightly import of scheduled tasks from the property system.
- `docs/`: operations and the task model.
