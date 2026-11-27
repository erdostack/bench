Decision: recursive-sql

Stand-ins are one lookup: the item_a of every row whose item_b is the ingredient, on the index that's already
there. Swaps are one way and don't chain, so nothing is ever walked; 5,400 rows and 40 views a minute is nothing
for SQLite. Stay on SQLite; a graph database would be a server for a lookup. I noted Marta's reading of the sheet in
docs/graph/DECISION.md, since the schema doesn't say which way a row goes.
