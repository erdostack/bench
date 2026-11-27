# chartgraph

The music catalogue graph behind the charts pages: artists, releases, the credits between them, and
weekly chart entries.

- `bin/sq <target> "<sql>"`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file.
- `changes/`: data changes for production, one file each, `NNNN_<what>.py`.
- `docs/targets.md`: which target is which. Read it before running anything.
