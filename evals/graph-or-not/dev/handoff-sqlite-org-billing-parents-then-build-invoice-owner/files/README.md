# billing-orgs

Customer organisations and who pays for what. Organisations nest (a group, its regional companies, their
departments). One SQLite database (`var/billing.db`, schema in `db/schema.sql`).

- `billing/db.py`: opening the database.
- `billing/invoices.py`: the monthly invoice run and the "who pays for this" tooltip in the admin UI.

Python 3.11+, standard library only.
