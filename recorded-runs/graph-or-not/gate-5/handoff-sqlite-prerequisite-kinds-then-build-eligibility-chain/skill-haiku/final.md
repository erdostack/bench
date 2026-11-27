Added `sql/prerequisite_chain.sql`. Given `:course_id`, it returns one column, `course_id`, for every course that belongs on that course's "everything you need before you can take this" list. The starting course is never in the result.

It is a recursive SQLite query, as in `docs/graph/DECISION.md`:

- Required and concurrent edges are followed, at every level, so a concurrent prerequisite brings in the chain behind it. Recommended edges are never followed, so nothing reached only through a recommended edge is returned.
- It uses `UNION` on the course id, so the walk ends on loops such as the mutual required pairs in the catalogue. The starting course is then removed from the result.
- Results are ordered by `course_id`.

It is not wired into `advising/pages.py`. The TODO there is unchanged, since you asked for the SQL file only.

Checks: I ran it through `advising/db.py`'s `rows()` on an in-memory SQLite catalogue built from `db/schema.sql`. Hand-built cases covered a concurrent chain, a recommended-only branch, a mutual pair, and a loop back into another chain. A randomised test on 400 courses and 1,500 edges matched an independent walk for every course (0 mismatches). The real catalogue (`var/catalogue.db`) is not in the repo, so the query has not been run on it. The decision record asks for that run before release, along with a timing check.

Nothing else in the repo was changed, and `docs/graph/DECISION.md` is untouched.
