# drainage-desk

Small tools for the flooding desk. When a manhole floods, the desk looks up what drains into it so the crew
knows which gullies and lines to check.

- The asset team exports the sewer network to `var/drainage.db` once a month (not committed; tables in
  `db/schema.sql`).
- `python -m drainage.desk <node_id>` prints the report for one flooded node.
- `sql/upstream_draft.sql` is a first attempt at the upstream list; it is not wired in.
- Python 3.12, standard library only.
