Wrote merge_duplicates in flows/merge.py. The matcher's pairs chain (9 groups have three records) and aren't
ordered, so it first groups them (union-find), then per group keeps the record registered first, moves the
other records' edges onto it (adding tonnes and deals when the kept record already has that edge), drops
edges between records of the same group so nobody sells to itself, and removes the others.
Check after running: `sum(1 for u, v in G.edges if u == v)` is 0 and the total tonnes, minus the dropped
in-group sales, is unchanged; count( ) of nodes goes from 520 to 471.
