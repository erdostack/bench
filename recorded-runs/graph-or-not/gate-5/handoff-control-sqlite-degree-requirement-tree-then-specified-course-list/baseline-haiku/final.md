I added `sql/requirement_courses.sql`. It takes `:requirement_id` and returns one `course_code` column with each code listed under that requirement or under any requirement nested inside it, at any depth, each code once.

It uses a recursive CTE that walks `requirement.parent_id` downward from `:requirement_id` (with `UNION`, so it also stops if the nesting ever loops), then joins that set to `requirement_course` with `SELECT DISTINCT`. The output is ordered by `course_code`, matching `direct_courses.sql`.

I checked it in SQLite against a small tree built from `db/schema.sql`. A top-level requirement returned codes from all its descendants, a middle requirement returned only its own subtree, a leaf returned its own codes, and an unknown id returned no rows. A course listed under both a parent and a child appeared once.
