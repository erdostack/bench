I added `sql/requirement_courses.sql`. It takes `:requirement_id` and returns one `course_code` column: each course listed under that requirement or under any requirement nested inside it, at any depth, once each, sorted by code.

It walks down `requirement.parent_id` with a recursive CTE (using UNION, so the walk ends even on bad data), then joins to `requirement_course` and applies DISTINCT. It is SQLite syntax, like `sql/direct_courses.sql`. An unknown requirement id returns no rows.

Checks: I ran it on a small hand-built tree at several roots, and on 300 random trees against a brute-force walk for every root. All results matched. I did not touch `audit/views.py` (its TODO for the full requirement page is still open) or the database, which is not in the repo.
