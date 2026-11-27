# musiclib

Wexcombe Community Radio's music library graph in SQLite: tracks, artists and releases in `nodes`, which
artist and release each track belongs to and which rotation it is on in `edges`.

- `bin/mq <target> "<sql>"` (or `--file <file.sql>`): run SQL on a target from `config/targets.toml`.
- `bin/rebuild-scratch`: replace scratch with a fresh copy of library.
- `docs/targets.md`: the targets. `docs/imports.md`: how imports are tagged.
