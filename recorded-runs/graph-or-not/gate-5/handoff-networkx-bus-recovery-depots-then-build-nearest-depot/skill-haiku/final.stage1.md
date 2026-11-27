Decision: in-process-library

Use the networkx graph the app already has, not a graph database and not recursive SQL. The edge set is small: 8,100 segments (stated) load to about 4.5 MB (measured on a synthetic network of the stated size; the real var/roads.db was not in the repo), and a load per call took about 26 ms. The wrong depot comes from the code: nearest.py counts hops (no weight), and load() keeps only the last row when two segments join the same pair, so a bus-gate row can overwrite the legal road. Fix in code: weight by minutes, drop bus_gate = 1 for the lorry, keep the minimum minutes per pair.

Not measured: the real road network, the freshness and latency budget, and the number of processes that load the graph. The graph database option was rejected because the load does not justify a second stateful system. Recursive SQL is passed over because no measurement shows it meeting the need. Nothing in the repo was changed except the new file docs/graph/DECISION.md.
