Added `gross_requirements(conn, item_id, qty)` in `planning/requirements.py`. It returns `{bought-in item id: quantity}` for every part with `make_buy = 'B'` needed to make `qty` of `item_id`, rounded to 3 decimals.

It follows the recorded decision in `docs/graph/DECISION.md` (recursive SQL on the database already run):

- The query is a single `WITH RECURSIVE` walk in `sql/gross_requirements.sql`. Each BOM line on a path multiplies the quantity by `qty_per * 1.04` (4% scrap on every line). The walk stops at depth 11, and the results are summed per bought-in part.
- The 11-level cap and the 1.04 factor are constants at the top of `planning/requirements.py`.
- The top-level item's own quantity is not scrapped, since the record leaves that case open and I followed its literal rule.

Checks: I compared the function against a brute-force Python walk on a random 300-item SQLite BOM, for every root at quantities 1 and 7, with 0 mismatches. I also checked the depth cap on a 13-level chain. No files in the repo other than the two new ones were changed, and `docs/graph/DECISION.md` is untouched.

Not verified: the Postgres path. There is no Postgres server here. The query uses `:name` placeholders, the same as the existing `sql/` files and `planning/sqlfile.py`. The README says every query must run on both engines, so someone should run this against the Postgres copy. If psycopg does not accept `:name`, that would need a fix in `sqlfile.py` for all queries, not just this one.

Open questions for the planning lead: whether "11 levels" means 11 lines below the root (as implemented), and whether the scrap also applies to the works order's own top-level line (implemented as no).
