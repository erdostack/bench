Position: keep

Björn, we decided on recursive-sql for this. The folder table is around 400M rows and the pods only have
512 MB, so the tree will not fit in memory, and the recursive query benchmarked at 3 ms. Refreshing every
10 minutes would also serve stale data. Let's stick with the query.
