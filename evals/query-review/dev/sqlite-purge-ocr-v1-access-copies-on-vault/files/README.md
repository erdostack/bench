# reliquary

Digital-object graph for the county record office: archival objects, their master scans and the access
copies the public viewer serves. `nodes` holds objects and files; `edges` holds `has_file` (object to
file) and `derived_from` (access copy to the master it was made from).

- `bin/rq <target> "<sql>"` or `bin/rq <target> --file <file.sql>`: run SQL on a target from
  `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, one file each, `NNNN_<what>.py`.
- `docs/TARGETS.md`: what each target is. Read it before running anything.
