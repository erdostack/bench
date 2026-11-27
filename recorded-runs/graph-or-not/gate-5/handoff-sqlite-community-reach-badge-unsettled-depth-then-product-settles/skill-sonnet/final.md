Decision: recursive-sql

The call changes from need-more-information to `recursive-sql`: do the badge as a fixed two-step walk along `follow` on the SQLite database you already run, and don't move follows into Neo4j.

The numbers it rests on:
- Depth: 1 or 2 only, nothing further (agreed by Dana and the PM). The earlier open question was 2 against up to 6, and that is now settled.
- Timing: the two-step lookup takes 9 ms p95 on a copy of the database, against the 150 ms the badge gets. That is about 16.7 times of headroom (150 / 9).
- Size of the work: the average member has 6.4M / 380,000 = 16.8 follows. A two-step walk reaches about 16.8^2 = 283 rows from one side. That is a small set, and the `follow` primary key and the `follow_followed` index already serve both directions.
- Load: peak is about 70 profile views a second. At 9 ms each, that is about 0.63 s of query time per second if everything ran on one connection at the p95 figure. The mean is lower, and SQLite in WAL mode lets readers run side by side.

Jonas's case for Neo4j doesn't hold. It would add a second store to feed and run, for a need that SQLite already meets with a wide margin. His idea might matter if the badge ever goes deeper than 2.

I updated `docs/graph/DECISION.md`: the decision line, the settled depth and the 9 ms figure are in, the old 2-versus-6 wording is marked as withdrawn, and the "what would change this" list is rewritten. That is the only file I changed. I ran nothing myself, because there is no database copy in the repo, so the 9 ms is your figure.

Three things I could not find and which matter for the build:
- Whether the 9 ms was timed under peak load and for members with very many followers. A hub member is the case most likely to be slow.
- Whether a step follows the arrow only (the viewer follows someone who follows the member) or goes either way. Either way roughly doubles the edges walked. The TODO in `commons/profile.py` only says "through follows".
- What the badge shows when there is no 1- or 2-step connection.

Re-time the lookup with a hub member and a few concurrent readers before it ships. If it stays under 150 ms p95 at about 70 views a second, nothing else is needed. The same document lists what would reopen the decision.
