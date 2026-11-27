Decision: graph-database

Adopt a dedicated graph database (Neo4j, which you already trialled). Keep the weekly SQLite import as the source of truth and load the graph store from it.

Why, from your numbers:

- **It met the requirement on real questions.** The two-week trial on a copy answered 6-link questions in 2 to 8 s, under your 10 s limit. Analysts wrote their own patterns after a day. That matters because every question is different (mixed relation kinds and dates), so a fixed algorithm doesn't fit.
- **Tuning SQLite won't close the gap.** `linked_within` (the recursive CTE in `investigate/queries.py`) took 14 min even with the indexes. It carries a text path per row and expands every route from the start. Your own level-by-level search from both ends only got to 3 min 20 s, and it was slowed by hubs: addresses and formation agents with hundreds of thousands of links. A gap of 20x to 100x isn't tuning territory. Wim is right that SQLite is a sound store. It is the wrong engine for variable-depth, multi-kind traversal at this size.
- **An in-memory library doesn't fit.** networkx was estimated at about 95 GB on a 64 GB server. A compact library could fit 310M edges, but it still gives you one fixed algorithm per question, not ad hoc patterns. You would also be rebuilding a query layer for 25 analysts by hand.
- **"No graph" doesn't apply.** The question is path-finding across several relation kinds.

Before the budget round, I'd check these four things, because the trial result is the only direct evidence and I haven't seen its details:

1. The trial copy was the full 48M / 310M data, and the 2 to 8 s timings include the worst cases: questions that pass through the hub addresses and agents.
2. 25 analysts running questions at once still land under 10 s on the 64 GB server. The trial may not have tested that load.
3. Date filters (`since` / `until`) and the "director or shareholder within 6 links of an official" question run at the same speed as the trial's plain 6-link questions.
4. The cost of the weekly reload from SQLite, the licence and edition terms for production, and who runs the database.

If check 1 or 2 fails, the answer is probably still a graph database, but you would need a larger machine or a different engine. It would not be SQLite.

I haven't changed anything in the repo.
