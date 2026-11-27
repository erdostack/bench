# learnswim

Wyfold Council's learn-to-swim programme as a graph in SQLite: pools, lessons, swimmers and instructors in
`nodes`, and what links them in `edges`.

- `bin/lsq <target> "<sql>"` or `bin/lsq <target> --file <file.sql>`: run SQL on a target in `config/targets.toml`.
- `scripts/build_practice.py`: build the practice database.
- `changes/`: reviewed data changes for live.
- `docs/targets.md`, `docs/model.md`.
