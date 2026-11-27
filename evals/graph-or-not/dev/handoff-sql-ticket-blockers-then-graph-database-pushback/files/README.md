# tracker-api

API behind the issue tracker's web app.

- Node 22, TypeScript, Postgres 16 (`pg`). Queries that are more than a line live in `src/panels/*.sql` and are
  loaded by `src/sql.ts`.
- `db/schema.sql` is the current schema (migrations are generated from it).
