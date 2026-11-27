Added best_route(conn, src, dst) to fx/route.py.

It reads the best provider rate for each pair from the cache and searches routes of at most three conversions
(two intermediate currencies), never passing through a currency in restricted_currency, and returns the route with
the best rate for the customer as (rate, path), or None. These are treasury's rules as recorded in
docs/graph/DECISION.md.
