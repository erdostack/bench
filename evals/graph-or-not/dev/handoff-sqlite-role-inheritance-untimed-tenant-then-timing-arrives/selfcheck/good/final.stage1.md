Decision: need-more-information

Sanne's rule makes this a measurement, not a debate: stay on SQLite while the indexed recursive query in
authz/effective.py meets the 3 s p95 budget, move role inheritance to the identity team's graph store if it misses.
On 39 of the 40 tenants it is 6 ms p95, nowhere near the line. The only tenant that could cross it is the
enterprise tenant, about 40x more roles and deeper inheritance, and it has never been timed.

What I need: the effective-permissions query timed on the enterprise tenant (p95, indexes in place) once its export
reaches the test box. Under 3 s, nothing moves; over 3 s, it goes to the graph store. Recorded in
docs/graph/DECISION.md.
