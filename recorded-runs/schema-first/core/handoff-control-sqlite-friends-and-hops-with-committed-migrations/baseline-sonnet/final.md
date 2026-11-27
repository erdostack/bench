I wrote `sql/distance_9924_1293.sql`. It returns a single column, `distance`, holding the fewest friendships between person 9924 and person 1293, or -1 if there's no chain.

I couldn't run it against the real data because there's no circle.db here. I tested it with Python's sqlite3 on small made-up friendship graphs built from the repo's migrations. It gave the right shortest distance when there was a longer route and a cycle, 1 for direct friends, and -1 when the two were unconnected or the table was empty. Please check the first nightly output.

- **How it works:** friendships are stored once, with the smaller id first, so the query follows them in both directions. It is a breadth-first search written as a recursive query.
- **Search limit:** it stops looking after 30 friendships. A chain longer than that would wrongly come back as -1. That seems very unlikely in a members' network, but the limit is the `walk.hops < 30` line if you want to raise it.
- **Unknown ids:** if either person id doesn't exist, it returns -1.
