I added `sql/requirement_courses.sql`. It takes `:requirement_id` and returns one column, `course_code`, for every course listed under that requirement or under any requirement nested inside it, at any depth. Each code appears once, sorted.

It uses a recursive query on SQLite, as `docs/graph/DECISION.md` recommends. It walks down `requirement.parent_id` from the given requirement. `UNION` and `DISTINCT` make sure a course listed under several requirements shows up once. It returns no rows for an unknown id.

I tested it on a small in-memory database built from `db/schema.sql`. That covered a three-level nesting, a course listed under two requirements, a leaf requirement and a missing id, and all behaved as expected. I couldn't run it on the real catalogue because `var/audit.db` isn't in the repo.

I did not call the new file from `audit/views.py`. I left that and `docs/graph/DECISION.md` unchanged.
