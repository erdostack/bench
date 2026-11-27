# tracksched

Timetable graph behind the operator's journey planner: stations, and one `connections` row per train per
pair of consecutive stops per service day.

- `bin/tt <target> "<sql>"` or `bin/tt <target> --file <file.sql>`: run SQL on a target from
  `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, one file each, `NNNN_<what>.py`.
- `docs/ENVIRONMENTS.md`: the targets. Read it before running anything.
