# provenance

Supplier and component records for the compliance team. Go 1.23, Postgres 16 (`pgx`).

- `internal/db/schema.sql` is applied by the migration job.
- Queries are in `internal/queries/*.sql` and embedded with `go:embed`.
- `cmd/report` renders the per-product supplier report compliance download from the admin.
