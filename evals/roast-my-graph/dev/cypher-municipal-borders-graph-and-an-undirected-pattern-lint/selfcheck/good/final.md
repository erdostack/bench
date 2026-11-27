None of the three needs changing. The loader stores each border once, and each query already handles
the fact that an undirected pattern can see a relationship from both ends: neighbours starts from one
municipality, so each neighbour comes back once; border_pairs keeps only the orientation where a's
code is lower; total_border_km divides by two, which is exact because a municipality never borders
itself (the loader skips those rows). The lint rule is right in general and wrong for these three.
