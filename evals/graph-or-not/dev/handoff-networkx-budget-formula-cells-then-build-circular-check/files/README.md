# ledgerbook

The finance team's budgeting workbooks. A workbook is a SQLite file (`var/*.db`, not committed) with one
row per cell and one row per reference from a formula to another cell (`db/schema.sql`). The web editor
calls `sheets.save.on_save(conn)` after every edit; it recalculates and runs the circular-reference check.

- Python 3.12, `pip install -r requirements.txt`.
- `pytest` runs the tests.
