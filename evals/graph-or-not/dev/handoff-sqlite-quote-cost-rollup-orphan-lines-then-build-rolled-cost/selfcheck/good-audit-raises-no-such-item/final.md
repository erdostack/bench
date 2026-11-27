quotecalc/rollup.py is in. rolled_cost(conn, item_id) walks down from the item and returns the rolled cost. If a
BOM line at any depth names an item that is not in the item table, it raises rather than quote a partial total,
per the record (no cost, never a partial total). The page should catch it.
