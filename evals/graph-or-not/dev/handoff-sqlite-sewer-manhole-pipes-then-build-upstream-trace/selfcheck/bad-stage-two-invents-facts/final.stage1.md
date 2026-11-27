Decision: recursive-sql

Stay on the SQLite export. Tracing what drains into one manhole is a walk upstream from one start node over
15,100 pipes, about 15 times a week: a recursive query handles that in milliseconds. The draft never finishes
because it carries a hop count, so every lap of the Eastgate overflow loops is a new row and UNION never sees a
repeat; carrying only the node id fixes it. The trace stops at pumping stations: neither the station nor
anything draining into it is listed. A graph database is a server to run for a monthly file and a laptop tool.
I wrote this down in docs/graph/DECISION.md.
