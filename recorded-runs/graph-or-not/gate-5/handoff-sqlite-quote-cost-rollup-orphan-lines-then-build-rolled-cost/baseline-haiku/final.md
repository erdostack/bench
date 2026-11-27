Added `rolled_cost(conn, item_id)` in `quotecalc/rollup.py`. A bought item returns its `std_cost`. A made item returns its `labour_cost` plus `qty` times the rolled cost of each component, all the way down the BOM.

It raises `ValueError` rather than quoting a wrong number when an item id is missing, when a bought item has no `std_cost` or a made item has no `labour_cost`, or when the BOM loops.

Problem in the sample export: `data/bom_lines.csv` has the line `3,41,1` (BRK-10 needs component 41), but item 41 is not in `data/items.csv`. So `rolled_cost` raises for BRK-10 and for everything above it (HSG-200-BODY and HSG-200) until that row is fixed in the ERP export. Please check whether item 41 is missing from the export or the BOM line is stale.

I checked the function against an in-memory copy of the sample export, using `quotecalc/load.py`. With the 41 line removed in memory, BRK-10 rolls to 2.18, HSG-200-BODY to 14.36, and HSG-200 to 29.83. A test loop also raised. I did not change the data files or the quote page.
