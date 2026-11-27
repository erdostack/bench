Added quotecalc/rollup.py. rolled_cost walks the BOM with one recursive query, multiplying quantities down the
levels; if any line below the item points at an item that isn't in the item table it returns None (finance's
rule in docs/graph/DECISION.md: incomplete, never a partial total).
