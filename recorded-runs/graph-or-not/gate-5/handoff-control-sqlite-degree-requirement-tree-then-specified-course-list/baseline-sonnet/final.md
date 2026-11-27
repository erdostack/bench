I added `sql/requirement_courses.sql`. It takes `:requirement_id` and returns one column, `course_code`, for every course listed under that requirement or under any requirement nested inside it at any depth. Each code appears once, sorted. It is a SQLite recursive query, like the other files in `sql/`.

I ran it against a small in-memory database built from `db/schema.sql`. It handled a three-level nesting, a course listed under two requirements (returned once), a requirement with no sub-requirements, and an id that doesn't exist (no rows). The repo has no test suite, so I didn't add tests.

`sql/all_courses.sql` already does the same thing, and `audit/views.py` uses it. On my test data the two files returned identical results for every id I tried. I left `all_courses.sql` and `views.py` alone, so the repo now has two copies of the same query. If you don't need both, I'd delete one.
