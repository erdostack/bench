Added seminar/groups.py. close_groups(conn) uses the definition in docs/graph/DECISION.md: pairs of women with at
least 4 shared events (networkx weighted projection), then the connected components; women with no close tie
are left out. On the Southern Women data it gives two groups, of 8 and 6.
