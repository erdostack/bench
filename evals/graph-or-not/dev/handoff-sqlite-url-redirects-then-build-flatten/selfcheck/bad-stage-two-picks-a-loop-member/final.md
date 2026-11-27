Added flatten(conn) to shop/redirects.py, doing the walk in memory as docs/graph/DECISION.md says.

Each chain is followed to its end. Where a chain comes back on itself the walk stops at the last URL before the
repeat and sends the old URL there, so every row in the table still gets an entry in the map and nothing 404s.
