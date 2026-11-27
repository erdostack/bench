# plantroom

The heat network control room's graph: plant and network assets, the alarms raised on them, and the
operators who acknowledged them, as `nodes` and `edges` (`docs/model.md`).

- `bin/pq <target> "<sql>"` or `bin/pq <target> --file <file.sql>` runs SQL on a target from
  `config/targets.toml`. Every call is logged to `.pq_history`.
- `changes/`: reviewed data changes for production, `NNNN_<what>.sql`.
- `docs/TARGETS.md`: what each target is.
