Decision: in-process-library

Build the account links in memory with networkx (already installed) after each nightly copy, and look up the connected component of the account. Do not move to a graph database.

What it turns on:
- Why the panel misses people: `linked_accounts` stops at `max_depth=3`, so groups chained further are cut off. Your own check agrees: 31 of 400 groups are affected.
- A second bug is in the same query: it joins on every signal kind, so a shared IP does link accounts today, against Ayla's rule. The graph must be built only from `signal` rows with `kind IN ('device', 'card')`. An IP then never links two accounts, alone or with something else.
- Size: 1.1M signal rows at most, 240k accounts, 200 lookups a day on a nightly copy. I measured a synthetic networkx graph of about that size at roughly 0.6 GB (about 550 bytes per edge; real data will differ), which is fine for one process. That leaves no size, load or freshness problem for a second database to solve.

What I could not find or measure: there is no database copy in the repo, so I did not measure real group sizes, the real build time, the host's memory, or how many processes serve the panel. Shared devices and cards (internet cafes, shared cards) can make some groups very large. Check the largest group on last week's copy.

Recursive SQL on SQLite might also be fast enough, and it would be the cheaper rung, but no one has measured it here, so I did not choose it. If you run one recursive query (`UNION` on account ids, device and card only) against last week's copy and the largest group comes back in well under 2 seconds, it would replace the in-memory build.

I wrote the decision to docs/graph/DECISION.md. Nothing else in the repo was changed.
