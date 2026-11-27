# gatekeeper

Authorisation service: answers "may this user do this to that resource" for the other services.

- Node 22, TypeScript, `pg` against Postgres 16.
- Migrations in `db/migrations`, applied in order.
- `src/check.ts` is the hot path; everything else is CRUD around it.
