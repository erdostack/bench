I added `families_within(conn, family, k)` in `seminar/reach.py`.

It walks outward from `family` one tie at a time, up to `k` steps. It treats each tie as running either way, so it doesn't matter which side of `marriage_tie` the family is on. It returns the sorted names of the other families it reached. The family itself is never in the list. You get an empty list for `k = 0`, for a family with no ties (such as the Pucci), and for a name that isn't in the table. A negative `k` also gives an empty list.

I only checked it against a small in-memory database built from `db/schema.sql` (a chain A-B-C-D plus an isolated E). The results were right for `k` of 0, 1 and 2, for a family in the middle of the chain, for a large `k`, and for the isolated family. I didn't build `var/seminar.db` or run it against the Florentine data, and the repo has no test suite, so I didn't add tests.

I didn't change `app.py`. Its reach endpoint still does its own counting with networkx.
