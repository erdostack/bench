Decision: recursive-sql

Stay on SQLite. The badge now only looks 2 steps, so it is a fixed lookup on the indexed follow table. You measured
9 ms p95; the badge's budget is 150 ms of the page at a peak of about 70 views a second (380k members, 6.4M follows).
That is a sixteenth of the budget. Moving follows into Neo4j would add a second store for a lookup SQLite already
answers. I updated docs/graph/DECISION.md from need-more-information to this.
