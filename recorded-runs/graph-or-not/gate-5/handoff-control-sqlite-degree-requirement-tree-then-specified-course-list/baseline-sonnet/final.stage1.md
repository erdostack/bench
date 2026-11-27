Decision: recursive-sql

Keep this in SQLite with a recursive query. Do not load the catalogue into Neo4j, and do not add a graph library.

Why:
- The data is small: 1,900 requirements, 14,000 listings, at most 5 levels. A subtree walk touches a handful of rows.
- `requirement.parent_id` is already indexed (`requirement_parent`), and `requirement_course` is keyed by requirement, so each step of the walk is an index lookup.
- The load is modest: about 2,000 views a day in registration week and almost nothing otherwise, which is well under one request per second on average.
- The importer already guarantees the nesting is a tree, so the recursion cannot loop.
- Neo4j would add a second database to run, secure and back up, plus a per-term sync from the catalogue, for a query that SQLite handles directly. "Requirement trees are graphs" is true, but a 5-level tree rollup is a standard recursive-query case.

What I did:
- Added `sql/all_courses.sql`, a recursive query that returns every course counting toward `:requirement_id`, including all sub-requirements, each course once and sorted.
- Filled in the TODO in `audit/views.py`. `requirement_page` now returns `{"direct": [...], "all": [...]}`. The `direct` key is unchanged.
- Checked it on a small made-up catalogue in memory: a course listed under several sub-requirements appears once, a leaf requirement returns its own courses, and an unknown id returns an empty list. I did not run it against a real `var/audit.db`, so I have not timed it, but at this size I expect no problem.

Notes:
- The page contract change is the new `all` key. If the template expects a different shape, tell me and I will adjust.
- If the page ever needs to show which sub-requirement each course came from, extend the query to return the requirement id and title alongside the course code.
