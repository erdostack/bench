# ledger-queries

Ad-hoc and scheduled SQL for the payments ledger. The ledger is a SQLite file; `var/ledger.db`
is last night's snapshot (about 12,000 accounts and 53,000 transfers).

## Running a query

    ./gq "SELECT count(*) FROM transfers"
    ./gq -f queries/top_senders.sql -p since=2026-10-01

`gq` reads `gq.toml`, logs every statement to `.gq_history`, and interrupts anything that runs
longer than `statement_timeout_s`.

## Tables

See `schema.sql`. A transfer moves money from `src` to `dst`; both are `accounts.id`.
The same pair of accounts can have many transfers.

## Conventions

- One statement per file in `queries/`, named parameters (`:name`), a header comment saying what it returns.
- Queries are read-only.
