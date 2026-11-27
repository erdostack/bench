Added flatten(conn) to shop/redirects.py. write_map is unchanged for now, as you asked.

It reads the redirect table once and follows each chain to the page at its end. Per docs/graph/DECISION.md, chains
can loop (the audit found 214) and the agreement with SEO is that a URL whose chain loops is left out of the map
entirely, so flatten drops those, and also URLs whose chain runs into a loop further down. Each path is walked once;
results are reused for URLs that join a chain part-way.

Checked on a SQLite db with a self-redirect, a two-URL loop, a chain into a three-URL ring and ordinary chains of up
to 6 hops.
