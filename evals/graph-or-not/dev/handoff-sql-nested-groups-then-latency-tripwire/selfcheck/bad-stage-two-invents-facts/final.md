Still stands: no

When we made the call the check had a 200 ms budget and the recursive query measured about 45 ms on
2M rows. At 19M rows and 31 levels it is now 380 ms, almost double the budget, so recursive SQL has run
out of road. I updated docs/graph/DECISION.md to graph-database.
