Added `sql/prerequisite_chain.sql`. It takes `:course_id` and returns one column, `course_id`, for every course on that course's prerequisite list. The course itself is excluded, and rows are ordered by id.

I took "the list we decided on" to be the rule already in `sql/all_prerequisites.sql`, since I wasn't sure which rule you meant:
- 'required' and 'concurrent' rows are followed all the way back.
- 'recommended' rows are never followed. A course that is only reachable through one doesn't appear.
- Cross-listed loops are handled by a `UNION` on the id alone, with no depth or path column. Because of that, the course can come back round to itself, and the final `WHERE` filters it out.

If the list should be different (for example, direct prerequisites only, or recommended ones included), it's a one-line change to the `WHERE p.kind IN (...)` filter or to the recursion.

It's plain SQLite and uses only `:named` parameters. I ran it by hand on an in-memory database built from `db/schema.sql`. A chain including a concurrent link and a loop back to the starting course gave the expected ids. A course reached only via a recommended row was left out, and a course with no prerequisites returned nothing. I didn't add a test file.
