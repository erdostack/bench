Decision: graph-database

Depth 4 is the case the earlier decision said to measure, and the measurement fails it: 870 ms p95 against the
120 ms the line gets, at 2,400 profile views a second, with replica lag climbing to 40 s while 4,500 new
friendships a second keep arriving. More indexes or a bigger instance would have to bring it down more than
seven-fold while also keeping replication current; that is not a tuning margin. Holding the 1.9 billion
friendships in our own services is ruled out by the 2025-06 incident and the platform review, so the line moves
to a graph database (Ines's proposal), fed from the knows change feed, with Postgres staying the system of record.

I will update the record once Ines has a plan.
