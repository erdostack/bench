Decision: in-process-library

Your two new measurements settle it. The earlier record said need-more-information only because the Brno and Pune sizes were unknown.

- Time: all 40,000 where-used lookups took 3 minutes (180 s), which is 30% of the 10-minute budget. The current recursive SQL would take 40,000 x 90 ms = 60 minutes, and that is Linz alone.
- Memory: 1.4 GB resident for 1.2M lines is 70% of the 2 GB allowance. That is about 1,167 B per line, so the allowance tops out around 1.7 million lines. That is only about 1.4 times today's size, so the margin is real but not large.
- A graph database is not justified when the in-memory pass already meets both limits. Recursive SQL is closed because it was measured at 6 times over budget.

Caveats:
- I ran nothing. There is no database or export in the repo, so the 1.4 GB, 3 minutes and 1.2M are your figures.
- I don't know whether the 3 minutes includes the per-assembly `retime` calls, or what the load time is. Time the load and the full run end to end on the production host before relying on the 180 s.
- More than one copy per host would exceed the allowance.

I updated `docs/graph/DECISION.md` with the new facts, the decision and the conditions that would reopen it. I changed no code.
