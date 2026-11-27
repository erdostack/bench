# storesgraph

Where every object in the museum's collection is: galleries, stores and the offsite store, as `nodes`,
with `located_in` edges. The movement app, the conservation team and the loans desk use it.

- `bin/cq <target> "<sql>"` or `bin/cq <target> --file <file.sql>`: run SQL on a target (`config/targets.toml`).
- `bin/apply <target> changes/<file>.sql`: apply a change file.
- `changes/`: data changes, one `.sql` file each. See `docs/changes.md`.
