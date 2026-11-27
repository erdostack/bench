# fair-admin

Admin scripts for the regional schools science fair. The registration site exports `var/fair.db` (not
committed; tables in `db/schema.sql`) once registration closes.

- `python -m fair.export` assigns judges to projects and writes `var/judging_sheets.csv` for the printer.
- Python 3.12. `pip install -r requirements.txt`.
