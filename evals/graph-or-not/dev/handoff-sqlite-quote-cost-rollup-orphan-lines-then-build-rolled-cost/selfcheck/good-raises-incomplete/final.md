quotecalc/rollup.py is in. rolled_cost(conn, item_id) walks down from the item and returns the rolled cost; if
any component at any depth is not in the item table it raises IncompleteCost instead of returning a number, per
the record (no cost, never a partial total). The quote page should catch IncompleteCost and show "incomplete".
