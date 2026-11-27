# shopfront

Product pages and cart for the homeware shop.

- Python 3.12, Flask. Postgres 16 in production; tests use SQLite built from `db/schema.sql`.
- SQL lives in `sql/*.sql`, one statement per file, named parameters (`:product_id`), and must run unchanged on
  Postgres and SQLite. `shopfront/sqlfile.py` loads them.
- Proposals go in `docs/proposals/`.
