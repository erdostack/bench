Decision: recursive-sql

Stay on SQLite. This is a bounded "everything below one item" walk, and it doesn't justify a graph database or a graph library.

Why:
- Size: 9,000 items, 31,000 BOM lines and 7 levels is small. A quote touches one item's subtree, and about 200 quotes a day is nothing.
- Index: `bom_line`'s primary key `(parent_id, component_id)` already indexes the lookup by parent. No new index is needed.
- Moving the BOMs to a graph database would not fix the dangling references. They come from a purge in the ERP export. A graph database with real edges would just refuse to load those ~300 lines, or silently drop them. Dropping them would give assemblies a partial total, which is exactly what Finance forbade. The cleanup belongs in the export or the loader, not in a new database.
- A graph library would mean loading all 31,000 lines into memory and keeping them in sync with the SQLite file. That's more moving parts for no gain.

What I changed (`quotecalc/quote.py`):
- `rolled_cost()` finds every item under the quoted one with a `WITH RECURSIVE ... UNION` query. Only made items are expanded. `UNION` removes repeats, so a subassembly used on many paths is visited once and a cycle in bad data can't loop. It then rolls the cost up with a memo: bought = `std_cost`, made = `labour_cost + sum(qty * component cost)`.
- A component id with no row in `item`, or a node with no cost, makes that item and every assembly above it return `None`. There is never a partial total. `quote()` returns `unit_cost=None` plus `incomplete=True` for the page to show. The page template isn't in this repo, so I didn't touch it.
- I first tried a pure recursive-CTE that multiplied quantities down every path. It blows up when subassemblies are shared, so I dropped it for the version above.

Checks:
- On the sample export, item 3 points at missing item 41, so items 1, 2 and 3 all come back `None`, while bought items 4, 5 and 6 are fine. After adding item 41, the costs come out at 3.18, 16.36 and 31.83, which match my hand calculation.
- On a synthetic 9,000-item, 30,000-line, 7-level BOM with a few items deleted, 200 quotes ran in about 0.12 s, with 9 of the 200 incomplete.
- I did not run it against the real export.

Worth doing separately: have `load.py` report the orphan lines it loads, so Finance can see which items were purged. I did not add that. I'd also leave `PRAGMA foreign_keys` off until the orphans are cleaned up, because turning it on now would reject the data.
