# Graph decision

Decision: recursive-sql

The academic family tree page walks advisors back through up to 19 generations of 41,000 researchers, and the question was whether to move it into a graph database before the national dissertations register arrives next year. What runs today already meets the need: the recursive query in SQLite answers the tree page at 18 ms p95 against the graduate school's budget of 250 ms, so the decision is the label for what is there and nothing needs to change.

## Workload facts

- 41,000 researchers, 46,500 advising rows (co-advised dissertations have two rows), deepest lineage 19 generations (stated by the user)
- Edges per researcher = 46,500 / 41,000 = about 1.13 advising rows each (stated by the user, divided)
- Fan-out is upward and small: each student has one advisor row, or two with a co-advisor (db/schema.sql, comment on `advising`; primary key `(student_id, advisor_id)`)
- Question asked: ancestors of one researcher with the generation each first appears, a walk of data-dependent depth along `advising` between researchers (sql/ancestors.sql)
- The query carries a path string and stops at 30 generations, so a data-entry loop cannot run forever; this guard was added after 3 loops from data-entry errors last year (stated by the user; sql/ancestors.sql)
- Index on the column the walk enters by: `advising_student` on `advising (student_id)` (db/schema.sql)
- Measured: the tree page runs at 18 ms p95 (stated by the user)
- Budget: 250 ms for the tree page, set by the graduate school (stated by the user). Headroom = 250 / 18 = about 14 times.
- Load: about 6,000 views a day (stated by the user), which is 6,000 / 86,400 = about 0.07 views a second averaged over the day; at 18 ms each that is far below one statement running at a time
- Agreement between the user and Tomasz: if the tree page goes past 120 ms p95, look at a graph database properly, and not before (stated by the user)
- The query returns one row per route: with co-advisors a researcher reachable by two routes comes back twice before `GROUP BY`. At 41,000 researchers and 1.13 rows each, lineages stay small, and this is already inside the 18 ms (sql/ancestors.sql, `GROUP BY r.id, r.name`).
- Freshness: the database is rebuilt nightly from the dissertation records by `lineage/build.py`, so answers are a day old by design (README.md)
- Operated today: Python 3.12 and SQLite, one file `var/lineage.db` (README.md)
- unknown: the size of the national dissertations register that arrives next year (researchers and advising rows); the request gives none, so no forecast is made
- unknown: how the 18 ms p95 was measured (the window and whether it includes the deepest lineages); only the user's figure exists, and there is no log or plan in the repo
- unknown: the query plan; there is no database copy in the repo and nothing was measured

## Options considered

- graph-database (a dedicated store, Tomasz's proposal "because genealogies are graphs"): rejected, because the current query meets the need with a 14 times margin (18 ms against 250 ms), the data is rebuilt nightly in SQLite anyway, and a second store would add a feed from the nightly build to keep in step.
- in-process-library (the data in memory with a graph library): rejected, because nothing is failing and it would add a load step and a copy per process for no gain over the 18 ms query.
- recursive-sql (the recursive query in SQLite that runs today): chosen, because it is measured at 18 ms p95 against a 250 ms budget on 41,000 researchers and 46,500 advising rows, with the index on `advising (student_id)`. Change nothing.
- no-graph (plain joins): rejected, because the lineage is followed for up to 19 generations, a walk of data-dependent depth that a fixed number of joins cannot express.

## What would change the decision

- The tree page passing 120 ms p95 on the production data (the threshold the user and Tomasz agreed) would trigger a proper look at a graph database, starting with a trial on the full register and the real mix of pages; the agreed trigger is the team's own and is not a failing budget (the budget is 250 ms).
- The national dissertations register arriving and the p95 staying under 120 ms would keep this unchanged. A measurement on the loaded data is the first thing to take after the import.
- The tree page p95 passing 250 ms, the graduate school's budget, with the cheaper remedies tried (the route-per-row result, the 30-generation cap) would move this away from recursive-sql.
- Lineages that need the whole register walked, for example descendants of a famous advisor over thousands of students, or a whole-graph analysis, would be a different question and should be sized separately.
