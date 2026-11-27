Decision: in-process-library

14,200 nodes and 15,100 pipes fit in memory many times over: load them into networkx in the desk tool and take
the ancestors of the flooded node, after removing pumping stations (the trace stops there, and neither the station
nor what drains into it is listed). networkx does not mind the Eastgate loops. No graph database. Written up in
docs/adr/0003-upstream-trace.md.
