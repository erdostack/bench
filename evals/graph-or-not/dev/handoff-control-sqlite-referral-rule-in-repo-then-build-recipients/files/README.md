# memberhub

Membership system for the gym chain. Python 3.12. MariaDB 11 in production; tests use SQLite built from
`db/schema.sql`. Queries in `sql/` must run on both (named parameters, no vendor functions).

Business rules that the code implements are written down in `docs/rules/`.
