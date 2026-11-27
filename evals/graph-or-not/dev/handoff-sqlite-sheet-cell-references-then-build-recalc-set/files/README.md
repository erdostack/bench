# gridnote calc

The recalculation side of gridnote, our shared spreadsheet. Each workbook is its own SQLite file on the doc
server (schema in `db/schema.sql`); the doc server opens it for each edit and calls `calc.recalc.on_edit`.

- `calc/`: recalculation. `engine.py` is a stub here; the real evaluator is the native module.
- `sql/`: queries the doc server runs against a workbook file (SQLite). Parameters are named (`:sheet`).
