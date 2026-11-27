# orgbook

Customer organisations and their subsidiaries, for the account pages and the nightly revenue rollup. One SQLite
database (`var/orgbook.db`, schema in `db/schema.sql`), loaded from the CRM every evening.

- `accounts/subtree.py`: the account page's "group structure" panel (an organisation and everything under it).
- `rollups/rollup.py`: nightly job, revenue summed up each organisation's subtree into `org_rollup`.

Run the rollup with `python -m rollups.rollup var/orgbook.db`. Python 3.11+, no third-party packages.
