I added `families_within(conn, family, k)` in `seminar/reach.py`, a new module in the work directory.

It loads every marriage tie, treats each tie as undirected, and runs a breadth-first search from `family` that stops expanding at depth `k`. It returns the sorted names of the families it reaches, without `family` itself. It returns `[]` when there are none, when `k` is 0, and when `k` is negative. A family that is not in the table gets `[]`.

I checked it on a small in-memory database with the schema from `db/schema.sql`: k = 0 gives `[]`, k = 1 gives the direct neighbours, k = 2 adds the next ring, and an isolated family gives `[]`. I did not run it against `var/seminar.db` because that file is not in the work directory.
