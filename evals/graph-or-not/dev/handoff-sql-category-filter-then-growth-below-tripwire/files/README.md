# catalog-search

Search and browse API for the marketplace. TypeScript on Node 22, Postgres 16 through `pg`.

- `src/` service code, `sql/` the statements it runs (loaded by `src/sql.ts`).
- `npm test` runs against a disposable Postgres in CI.
