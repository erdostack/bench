Added `gross_requirements(conn, item_id, qty)` in `planning/requirements.py`. It walks the BOM all the way down, multiplying `qty_per` at each level, and returns `{item_id: quantity}` for every `make_buy = 'B'` part, rounded to 3 decimals.

Notes:
- Bought-in parts are leaves, so their own BOM lines are not exploded.
- If the requested item is itself bought-in, it returns `{item_id: qty}`.
- A missing item id raises `ValueError`, and so does a BOM cycle.
- It reads through the existing `sqlfile` and a new `sql/item_make_buy.sql`, so the queries stay portable between Postgres and SQLite.
- I checked it against an in-memory SQLite copy of `db/schema.sql` with a small two-level BOM. Results matched hand calculations, and the cycle and missing-item cases raise as described. I did not add a test file to the repo.
