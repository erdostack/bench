Position: keep

We decided to keep the recursive query on Postgres (recursive-sql). It drops a branch once its share is below
0.001, so it does not loop forever, and moving to a new database before year-end is a big risk for a report
that works.
