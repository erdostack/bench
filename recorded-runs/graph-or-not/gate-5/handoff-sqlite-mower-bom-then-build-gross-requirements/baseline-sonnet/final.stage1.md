Decision: recursive-sql

Stay on Postgres and use a recursive query. You already measured it: 0.4 s for your biggest ride-on mower, against a 3 s target. At 300 runs a day on 210,000 BOM lines, a graph database or an in-memory graph library would add a second copy of the BOMs to keep in sync with the nightly PLM load, for no gain. Your BOMs are copied nightly from PLM into Postgres, so the data is already in the right place, with an index on `bom_line(component_id)` plus the primary key on `(parent_id, component_id)` for the downward walk. The consultant is right that a BOM is a graph, but a BOM explosion is a plain downward walk with a multiplier, which is what recursive SQL is for.

What I added:
- `sql/gross_requirements.sql`: takes `:item_id` and `:qty`. It walks down from the item and expands only made items (`make_buy = 'M'`). The running quantity is multiplied by `qty_per * 1.04` on every BOM line, so 4% scrap compounds down the levels. A part three levels down carries 1.04 cubed, and the order quantity itself gets no scrap. A bought part used on several paths is summed, and the result is one row per bought part: `id, part_no, description, uom, required`. It follows the repo's rule of working on both Postgres and SQLite, and it has a depth cap of 25 as a backstop against a loop in the PLM data.
- `planning.orders.gross_requirements(conn, item_id, qty)` runs it, and I removed the TODO.

Checks, on a small SQLite test:
- A mower with a deck, two blades and four wheels, with steel and bolts at different depths and one bought part that wrongly has BOM lines of its own (those are ignored). For 100 mowers it gave steel 1730.56, bolts 865.28 and wheels 416.0, which match my hand calculation with 1.04 per level.
- I have no Postgres here and your data isn't in the repo, so I have not run it on Postgres. Please run `gross_requirements.sql` on your copy. Replace `:item_id` and `:qty` with the biggest mower and a real quantity.

What to watch:
- The query walks every path, not every distinct part. If one subassembly is used in many places, the same rows are visited once per path. Your 0.4 s says it is fine for the real data. On a made-up dense 11-level BOM I built, one top item took 6.7 s in SQLite and returned about 16,000 bought parts. If a real BOM ever gets close to that, the fix is to total each level by part, one SQL query per level (11 at most), rather than anything graph-shaped.
- Quantities come back as raw floating-point values. Rounding up to whole purchasing units is not done here, since I don't know your rule for it.
- The scrap rate is hard-coded as 1.04 in the SQL. If it needs to vary by line or part, it will need a column or a parameter.
- Cycles are not reported. A loop in the data is cut off at depth 25 and gives wrong numbers rather than an error. PLM should not produce loops, but a loop check on the nightly load would be worth adding.
