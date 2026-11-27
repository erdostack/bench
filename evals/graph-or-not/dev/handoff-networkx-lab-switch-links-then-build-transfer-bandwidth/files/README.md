# netops

Small tools for the research computing group's data-transfer network (the DTN hosts and the switches
between them).

- Python 3.12, `pip install -r requirements.txt`.
- Inventory: `var/inventory.db`, a SQLite file exported every night from the cabling spreadsheet (not
  committed). Tables in `db/schema.sql`: one row per device, one row per physical cable.
- `python -m netops.topology` draws the diagram on the wiki page.
- `netops/app.py` is the little Flask app on the ops VM.
