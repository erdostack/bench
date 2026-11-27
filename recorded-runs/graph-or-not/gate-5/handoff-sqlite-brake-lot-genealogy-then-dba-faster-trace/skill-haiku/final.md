Still stands: yes

Keep the graph database. Markus's covering indexes on the replica help, but they do not bring either trace near the 30 s OEM budget.

Old against new, on a full copy:

- Forward containment, recursive SQL: 14 minutes (840 s) before the covering indexes, 6 minutes (360 s) after. That is 28 times the budget before and 12 times now (derived: 840 / 30 and 360 / 30). The change is 2.3 times faster (derived).
- Backward root cause, recursive SQL: not recorded before, 4 minutes (240 s) now, 8 times the budget (derived: 240 / 30).
- Graph database trial, for comparison: 1.2 s forward and 0.9 s backward. Both are within 30 s with headroom.

Why the call holds: the Postgres walk is still measured failing at the required 30 s, and a change that has now been run is still failing, so the rung stays rejected. The write rate is still about 3,000 links a second, so the 2.3 billion links keep growing by about 259 million a day. The in-memory option is still far above the 64 GB host limit.

Caveats to check before the spend is final:

- The 6-minute and 4-minute figures are yours. The repo does not show the covering indexes: `db/schema.sql` still has the plain indexes, so the layout is unverified here.
- Each figure needs its run count or percentile, and the replica should match production load. Both are unknown.
- The 30 s budget is the OEM contract. Relaxing it to around 6 minutes would be a contract change for the OEM contract owner and the quality team, not a database decision. If that happens, the recursive SQL option would be the one to revisit.

I updated `docs/graph/DECISION.md` in the work directory with the new numbers beside the old. The Decision line still reads `graph-database`. Nothing else in the repo changed.
