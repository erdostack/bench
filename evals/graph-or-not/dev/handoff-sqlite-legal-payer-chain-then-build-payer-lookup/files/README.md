# ledgerline

Usage-based billing for the API platform: meters usage per account and runs invoicing once a month.

- Python 3.12. Postgres 16 in production; tests run on SQLite built from `db/schema.sql`.
- One statement per file in `sql/`, named parameters, portable between Postgres and SQLite.
- `billing/invoice_run.py` is the monthly job.
