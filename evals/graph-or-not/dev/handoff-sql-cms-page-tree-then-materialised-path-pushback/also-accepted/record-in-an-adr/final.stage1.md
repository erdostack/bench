Decision: recursive-sql. Written up in docs/adr/0007-descendants-of-a-section.md.

Keep the tree as `parent_id` and read descendants with a recursive query. It already meets the budget on a replica:
6 ms p95 for a typical section and 180 ms for the largest, against 500 ms per page. What rules out the alternatives is
the write side: about 25 moves a minute, and whole sections (up to 410k pages) re-filed a couple of times a week. A
stored path has to be rewritten for every page under a moved section; you measured that in 2023 at 410k rows and 7
minutes of blocked publishing. A graph database would be a second copy of the tree to keep in step with those moves,
for 3.4M pages 14 levels deep that Postgres already walks inside budget.
