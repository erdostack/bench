Added `sql/prerequisite_chain.sql`. It takes `:course_id` and returns one `course_id` column with every course needed before that course can be taken, at any depth. The course itself is never returned.

Decisions to check:
- Only `kind = 'required'` edges are followed. `concurrent` prerequisites are taken in the same term, and `recommended` ones are not needed, so neither counts as "needed before you can take this".
- The walk is transitive. If CHEM 210 requires MATH 201, which requires MATH 101, then MATH 101 is on CHEM 210's list too. Say if you only wanted direct prerequisites, since that would just be `sql/listed_prerequisites.sql` with the `kind` filter.
- It uses `UNION` rather than `UNION ALL`, so a cycle in the catalogue data terminates instead of looping.

I checked it against an in-memory SQLite copy of `db/schema.sql` with a small chain, a concurrent edge, a recommended edge, and a two-course cycle. Results matched expectations. I did not wire it into `advising/pages.py`, since the request was for the SQL file only.
