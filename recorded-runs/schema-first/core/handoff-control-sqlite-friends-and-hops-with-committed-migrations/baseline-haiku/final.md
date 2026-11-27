I wrote `sql/distance_9924_1293.sql`. It returns one number: the fewest friendships in a chain from person 9924 to person 1293, or -1 if there is no chain. It is a single SELECT, so it runs under the nightly sqlite3 job like the other reports.

I could not run it against circle.db because it is not on this machine. I tested it on a small made-up database with the same schema. It returned the right answer for a 4-hop chain, a direct friendship (1), an unrelated pair elsewhere in the data (the chain's answer is unchanged), and no friendships at all (-1).

Tonight, run it on the office PC and check that it returns a single row with one value.
