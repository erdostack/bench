Decision: recursive-sql

Keep the recursive SQL query in SQLite and change nothing. Moving the family tree pages to a graph database is not justified by what you have measured.

What it turns on:
- The tree page runs at 18 ms p95 against the graduate school's 250 ms budget, about 14 times of headroom, on 41,000 researchers and 46,500 advising rows (about 1.13 per researcher) and a deepest lineage of 19 generations.
- Load is about 6,000 views a day, about 0.07 a second on average, so concurrency is not a worry.
- The query already has the index it needs (`advising_student`), the 30-generation cap, and the path check that stopped the 3 loops. The data is rebuilt nightly in SQLite anyway, so a graph database would be a second store with a feed to keep in step.

"Genealogies are graphs" is true, but it is not a reason to move: this is a walk up the advisors to a modest depth over a small edge set, and your own measurement says SQL handles it.

I could not find the size of the national dissertations register, how the 18 ms p95 was measured, or the query plan. There is no database copy in the repo, so I measured nothing myself.

Keep your agreement with Tomasz as written: if the tree page passes 120 ms p95, look at a graph database properly, starting with a trial on the full register and the real page mix. After the register import, take a p95 reading first. The 250 ms budget is the point where recursive SQL would stop meeting the need.

I wrote the decision to docs/graph/DECISION.md. Nothing else in the repo was changed.
