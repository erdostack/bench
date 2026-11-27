Still stands: no

The decision rested on a flat class list. With 5 nested levels the check has to walk up the class tree, which a
recursive query on Postgres does easily at 21k drugs and 140k rules, within the 200 ms the check gets. So the call
moves from no-graph to recursive-sql; still no graph database.
