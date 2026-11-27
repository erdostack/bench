Added `gross_requirements(conn, item_id, qty)` in `planning/requirements.py`. It returns `{item_id: quantity}` for every bought-in part (`make_buy = 'B'`), rounded to 3 decimals.

It runs the existing `sql/gross_requirements.sql`, so it applies the rules already written there:
- 4% scrap on every BOM line, compounding with depth.
- No scrap on the order quantity itself.
- Parts used on several paths are summed.
- Only made items ('M') are expanded.

I assumed that file is the version we decided on. If the scrap rule has changed, the change belongs in that SQL file, because `planning/orders.py` already calls it too.

I ran it by hand against an in-memory SQLite database built from `db/schema.sql`. I did not add a test file.
- A two-level BOM with a part used on two paths gave the figures I worked out by hand: 75.296 and 21.632 for 10 units.
- An unknown item id returns `{}`.
- A bought item as the top item returns itself with no scrap.
