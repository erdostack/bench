Done. `sql/prerequisite_chain.sql` is written. It takes `:course_id` and returns one column, `course_id`, for every course on that course's prerequisite list. The starting course is not included. The rows are ordered by id.

It follows `docs/graph/DECISION.md` (recursive SQL on the existing SQLite catalogue):
- It follows `required` and `concurrent` rows all the way back. It never follows `recommended` rows, so a course reachable only through a recommended one is left out.
- It uses a plain `UNION` on the course id, with no depth or path column. Each course is visited once, so the 23 cross-listed required pairs (2-cycles) end instead of looping. The starting course is filtered out at the end, so a loop back to it doesn't put it on its own list.
- It uses SQLite syntax only, like the other files in `sql/`. I did not add or change any other file.

I tested it on a small in-memory SQLite db built from `db/schema.sql`. The cases were a mutual-required pair, a concurrent link, a recommended link with a required one behind it, a self-reference and a course with no prerequisites. All came out as the rule says. I did not run it on a real `var/catalogue.db` (it isn't in the repo), so there is no timing. The decision doc names a page latency budget from the advising web team as the open item.

The query is not yet called from `advising/pages.py`.
