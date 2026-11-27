Added `rolled_cost(conn, item_id)` in `quotecalc/rollup.py`. It returns the rolled-up unit cost of the item, as you specified: a bought item's `std_cost`, or a made item's `labour_cost` plus `qty` times the rolled cost of each component, summed over the whole BOM.

It follows the recorded decision in `docs/graph/DECISION.md` (recursive SQL on the database already run):

- One recursive query walks down the BOM to depth 7 (`MAX_DEPTH` at the top of the module), one row per path. Only made items are expanded, so a bought item's own BOM is never followed. Each path contributes its quantity product times the endpoint's own cost, which gives the same total as the recursive definition.
- Finance's rule is applied: if any item under the assembly is missing from the item table, the function returns `None` for that assembly, never a partial total. A missing `labour_cost` on a made item or a missing `std_cost` on a bought item also returns `None`, since I read a NULL cost as unknown. Items that do not exist return `None` too.

Checks, in memory only: the function matches a plain recursive reference on 400 random items, with orphan lines and missing costs included (0 mismatches). On the sample export, items 1, 2 and 3 return `None` because the sample BOM has an orphan line from item 3 to item 41, which is not in `items.csv`. Items 4, 5 and 6 are bought items and return their `std_cost` (3.8, 0.04 and 0.65).

Two things to decide before you wire the page:

- The walk stops at depth 7 as the record says. If a real assembly goes deeper than that, its cost is cut short silently, not returned as `None`. Tell me if you want that case flagged instead.
- I treated a NULL labour or std cost as unknown (`None`). If some made items legitimately have no labour, the rule needs changing.

The `TODO` in `quotecalc/quote.py` is unchanged, since you said you would wire the page. Nothing else in the repo was changed, and `docs/graph/DECISION.md` is untouched.
