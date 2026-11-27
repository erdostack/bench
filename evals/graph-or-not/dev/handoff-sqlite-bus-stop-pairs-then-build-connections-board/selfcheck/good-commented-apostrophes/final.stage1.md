Decision: no-graph

The Connections panel is a lookup: the stop, the stop across the road (one row of stop), and the routes calling
at either (one join on stop_route), minus school-only routes. Nothing is walked beyond that, whatever the depth of
the network. 41,000 stop-route rows in a nightly SQLite file, read by 1,200 screens once a minute, is an indexed
query. A graph database would be a second copy of the timetable to keep in sync every night. Recorded in
docs/graph/DECISION.md with the rules customer services gave.
