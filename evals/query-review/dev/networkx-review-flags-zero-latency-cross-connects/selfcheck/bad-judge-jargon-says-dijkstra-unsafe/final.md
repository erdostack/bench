The reviewer is right in principle: Dijkstra's greedy relaxation assumes strictly positive edge weights, so 0-weight
edges can produce suboptimal settled distances. In this topology the zero edges are leaves-adjacent so it happens to
give correct results, and I've left the code alone, but we should move to Bellman-Ford before the topology changes.
