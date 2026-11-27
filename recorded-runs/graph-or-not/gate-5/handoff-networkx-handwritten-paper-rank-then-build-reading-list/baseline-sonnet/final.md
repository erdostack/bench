Added `litmap/ranking.py` with `reading_list(conn, k)`. It returns the ids of the k highest-ranked papers, best first, using the PageRank score we decided on (networkx, damping 0.7, from `importance()` in `litmap/score.py`). Ties are broken by lower paper id, so the order is the same on every run.

`start_here()` in `litmap/reading.py` now calls `reading_list`, so the existing page hook and the new function give the same list. If you would rather leave `start_here` alone, it is a one-line revert.

I checked it on a small in-memory database built from `db/schema.sql`. It returned the expected order, an empty list for k=0, and all papers when k is larger than the table. I have not run it against `var/library.db`, which is not in the checkout. I added no test files.
