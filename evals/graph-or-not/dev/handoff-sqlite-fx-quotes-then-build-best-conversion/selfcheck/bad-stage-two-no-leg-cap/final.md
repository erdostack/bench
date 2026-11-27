Added best_route to fx/route.py. It builds the quote graph in networkx with weight -log(rate), leaves out
restricted currencies, and takes the Bellman-Ford shortest path, which is the best overall rate.
