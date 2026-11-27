pipe_layout now picks runs cheapest first and skips any run that would close a loop (Kruskal), with track
crossings costed at length + 40 as the decision record says. No new dependency.
