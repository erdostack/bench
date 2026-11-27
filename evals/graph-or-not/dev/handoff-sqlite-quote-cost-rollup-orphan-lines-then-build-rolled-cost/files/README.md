# quotecalc

Quoting tool for the job shop: price a part from its routing and bill of materials.

- Python 3.12. Data is a SQLite file (`var/quotes.db`) rebuilt from the ERP CSV export by `quotecalc/load.py`;
  a sample export is in `data/`.
- `db/schema.sql` has the tables.
