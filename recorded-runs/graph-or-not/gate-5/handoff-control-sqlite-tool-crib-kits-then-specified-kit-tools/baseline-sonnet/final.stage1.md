Decision: recursive-sql

Stay on SQLite and use a recursive query. This is a small tree walk. It is not a graph-database problem.

Why:
- The data is tiny: 3,200 tools and 410 kits, nested at most 4 deep. A walk from one kit touches at most a few thousand rows.
- Traffic is about 50 views a day. Even a slow query is fine, and this one should take milliseconds.
- `kit_line` already has a primary key on `(kit_id, item_id)`. That index serves the `kit_id` lookup each recursive step needs, so no new index is required.
- A graph database would add a second datastore to run, sync and back up. The issue and return data stays in SQLite either way. An in-process graph library would mean loading the data into memory on each request, or keeping a cache that can go stale.
- Nothing here needs graph algorithms such as shortest paths, centrality or pattern matching. "Everything inside this kit" is a transitive closure over a containment tree, which `WITH RECURSIVE` handles directly.

What I changed in the working directory:
- Added `sql/kit_all_tools.sql`. It is a recursive CTE that walks `kit_line` down through nested kits. It multiplies `qty` down the nesting, so 2 kits of 3 drivers count as 6. It returns only `kind = 'tool'` rows, summed per tool. It has a depth guard of 8, so a cycle in the data can't loop forever.
- `crib/kits.py`: `kit_page` now returns `{"top": ..., "tools": ...}`, which resolves the TODO.
- I checked it on a small in-memory SQLite database with a nested kit, and the quantities came out as expected. I did not run it against the real `var/crib.db`, which isn't in the working directory, or run any Flask or project tests.

Revisit this only if the requirements change to things like where-used queries across the whole crib, compatibility or dependency reasoning, or nesting that gets much deeper, and even then recursive SQL is probably still enough. The automation engineer's instinct that kits inside kits are a graph is right in the abstract, but at this size SQL does the job.
