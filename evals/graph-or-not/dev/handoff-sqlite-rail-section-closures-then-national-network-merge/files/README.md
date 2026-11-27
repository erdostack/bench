# disruption-desk

Tools for the operator's disruption desk. The infrastructure register is exported every night to
`var/infra.db` (SQLite, not committed; tables in `db/schema.sql`).

- `disruption/desk.py <section_id>`: stations cut off from the core network if a track section closes.
- `sql/cut_off.sql`: the query behind it.
