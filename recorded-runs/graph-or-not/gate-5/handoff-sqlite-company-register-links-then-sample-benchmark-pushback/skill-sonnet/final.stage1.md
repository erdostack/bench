Decision: graph-database

Adopt a dedicated graph database (Neo4j, which you trialled). This is a real traversal problem: up to 6 links over 310M relations of 11 kinds, ad hoc questions, and an online budget of 10 s.

The numbers it turns on:
- SQLite recursive SQL: 14 minutes at 6 hops, killed, even with indexes and the path check. The level-by-level rewrite took 3 min 20 s. Both are far over 10 s, and the rewrite is already the tuned version of Wim's route. Hubs with hundreds of thousands of links are the cause.
- In-memory library: about 95 GB estimated against 64 GB RAM, and it is one fixed algorithm while every question is different. No leaner layout has been measured, so it is not shown to hold.
- Neo4j trial: 2 to 8 s on the same 6-link questions, and analysts wrote their own patterns after a day.

Before committing money, repeat the trial on the full 310M-relation set with the real mix of analyst questions, and check that the load fits your weekly import window.

I could not find in the repo or your message: the size of the trial copy and its hardware, how many of the trial questions were slower than 8 s, the write rate, and the Neo4j edition and cost at this size. I measured nothing myself, since there is no data copy here, only the 20,000-entity sample builder. I wrote the decision and its reasoning to docs/graph/DECISION.md. Nothing else in the repo was changed.

What would change this: a measured SQLite or in-memory build that answers 6-link questions in under 10 s at the 95th percentile on the full data, a trial on the full set that misses the budget, or a lower depth requirement.
