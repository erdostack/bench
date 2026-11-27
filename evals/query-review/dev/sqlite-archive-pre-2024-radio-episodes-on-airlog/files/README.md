# airlog

Wexcombe Community Radio's station database in SQLite: shows, presenters, tracks and broadcast episodes in
`nodes`, what links them in `edges`, and the archive tables (`docs/archive.md`). It started life as the
"air log" spreadsheet the studio kept, hence the name.

- `bin/aq <target> "<sql>"` (or `--file <file.sql>`): run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a change file (`docs/targets.md`).
- `changes/`: data changes.
