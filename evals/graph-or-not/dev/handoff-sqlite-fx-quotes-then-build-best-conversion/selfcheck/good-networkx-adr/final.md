best_route is in fx/route.py, using networkx as in ADR 0007: restricted currencies are dropped from the middle of the graph, then every simple path of up to 3 conversions is scored and the best rate wins.

I tried it on a toy cache of 5 currencies built in the shell; it picked the 2-leg route over the direct quote when that was better.
