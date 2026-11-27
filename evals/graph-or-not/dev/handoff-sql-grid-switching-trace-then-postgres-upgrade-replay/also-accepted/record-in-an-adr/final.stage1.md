Decision: graph-database

Every cheaper rung has been measured and misses. The recursive query, already with a loop guard and indexes,
replays the storm at 8.4 s p95 against a 1.5 s budget. In memory the grid is about 35 GB (2.1 GB for 6%) on 16 GB
servers, and splitting by region fails because 41% of storm traces cross regions after switching. A closure table
is 6.8 billion rows invalidated by 45,000 switching changes a day. A variable-depth walk over 3.4M segments that
changes all day is what a graph database is for. Recorded in docs/adr/0009-outage-trace-store.md.
