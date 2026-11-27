Decision: recursive-sql

Keep the catalogue in SQLite and do the walk with a recursive query. The data is tiny: 2,400 courses, 3,900 prerequisite rows, chains at most 7 deep, and a 1.5 MB file rebuilt each term. Course pages get about 3,000 views a day. A single-course walk over indexed rows takes well under a millisecond, so there is nothing to gain from a graph database or an in-memory graph library. Both would add a second copy of the data, plus either a load step or a service to run, for a query SQLite already handles. The `prerequisite_requires` index and the primary key on `(course_id, requires_id)` already cover the lookups. The standard library is enough.

**What I added**
- `sql/all_prerequisites.sql` follows only `required` and `concurrent` rows, all the way back. `recommended` rows are never followed, so anything reachable only through a recommended prerequisite is left out. A course that is also reachable through a required or concurrent chain is still listed.
- `advising/pages.py` now returns a `needed` list alongside `listed`: `(code, title, level)` rows sorted by level, then code. This replaces the TODO.

**Loops**
The cross-listed pairs that require each other are handled by the query shape. The recursive step carries only the course id, and `UNION` drops repeats, so a course already reached is not expanded again. Please don't add a depth or path column to that query. It would make every revisit a new row, and the walk would loop forever on the 23 cycles. The course itself is excluded from its own list, which also stops a cross-listed partner from listing the page's own course.

**Concurrent prerequisites**
I treated them like required ones when walking back: a concurrent course's own prerequisites are listed too, since the registrar wants the whole chain. I didn't encode the "must be passed by the end of that term" rule. The list only says what is needed, not when. If advising wants concurrent items marked on the page, the walk would need to carry the kind, and it's worth checking how that interacts with the loops first.

**Checks**
- There is no `var/catalogue.db` here, so I tested on a small in-memory database built from `db/schema.sql`. It had a required/concurrent loop, a recommended edge to a course with a required prerequisite behind it, and a recommended edge to a course that is also reachable by a required chain. The list came out as expected and the walk ended.
- I haven't run it against a real term's catalogue or timed it. I didn't add a test file.

**When to revisit**
If advising later needs questions SQL handles badly, such as shortest paths, "what does this unlock" across many courses at once, or degree-plan search, look again then. Nothing in this request needs it.
