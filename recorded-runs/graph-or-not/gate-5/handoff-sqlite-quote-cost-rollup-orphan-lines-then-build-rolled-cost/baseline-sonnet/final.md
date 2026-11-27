`rolled_cost(conn, item_id)` is now in `quotecalc/rollup.py`.

`quotecalc/quote.py` already had a `rolled_cost` with exactly the rule you described: a bought item costs its `std_cost`, and a made item costs `labour_cost` plus qty times the rolled cost of each component. It also had finance's incompleteness rule. So I moved that function into `rollup.py` instead of writing a second copy. `quote.py` now imports it from there, so `quote()` behaves as before and there is one definition. I didn't touch the rest of the page.

- **Incomplete costs:** it returns `None`, never a partial total, when anything under the item is missing. That covers a component id with no row in `item`, a bought item with no `std_cost`, a made item with no `labour_cost`, and a cycle in the BOM. This comes from the existing comment citing finance's rule, so I kept it.
- **Sample data:** HSG-200 (1), HSG-200-BODY (2) and BRK-10 (3) all come back `None`, because BRK-10 lists component id 41, which isn't in `items.csv`. PLT-55 gives 3.8, SCR-M5 gives 0.04 and GSK-200 gives 0.65.
- **Shared parts:** a subassembly used on several paths is only visited once.

I ran it by hand on the sample export. I didn't add a test file.
