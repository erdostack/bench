Position: keep

Femi, you're right about recursive SQL in general: a walk over a cyclic graph with no stopping rule never ends, in
Postgres or in Neo4j. Ours has one. The roll-up multiplies the shares along each chain and drops a branch once its
share falls below 0.1% of the original, and no retrocession in our book passes on more than 60%. So every lap of a
spiral at least shrinks the share by 40%, and after 14 steps any branch is below the cut-off. We have 14 spirals in
the book today and the query handles all of them.

It runs in 40 seconds of a 2 hour nightly window on 21,000 cessions, and it matched the actuaries' spreadsheet to the
cent at the 2025 year-end. So we decided to keep the recursive query on Postgres. A graph database would need exactly
the same cut-off, plus a second copy of the treaty data.
