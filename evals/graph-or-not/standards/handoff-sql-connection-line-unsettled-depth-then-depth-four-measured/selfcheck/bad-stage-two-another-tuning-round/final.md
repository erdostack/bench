Decision: recursive-sql

870 ms p95 is a first attempt. With a covering index on knows both ways and a bigger replica, a two-sided expansion
should come down a lot; the line gets 120 ms and 2,400 views a second is within what a larger Postgres replica can
take. Give Kemal his round before adding a second database. Updated docs/graph/DECISION.md.
