# rights-graph

Which film is available where: titles, territories, the licences between them, and the availability
edges the storefronts read. SQLite.

- `changes/`: data changes, `NNNN_<what>.sql`, applied in order by the release with
  `bin/apply-sql <db> changes/<file>`.
- `db/schema.sql`: the schema.
- `docs/licensing.md`: how licences and availability relate.
- `docs/tickets/`: tickets for data changes.
