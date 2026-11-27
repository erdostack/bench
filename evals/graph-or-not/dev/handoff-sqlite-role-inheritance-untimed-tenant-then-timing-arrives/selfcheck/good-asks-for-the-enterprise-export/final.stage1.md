Decision: need-more-information

Sanne's rule decides this: SQLite stays while the indexed recursive query in authz/effective.py meets 3 s p95,
and role inheritance moves to the identity team's store if it misses. The 39 small tenants are at 6 ms p95. The
enterprise one is about 40x bigger and deeper and is the only one that could miss.

Before anyone moves anything: get the enterprise export onto the test box and time effective.py on it, with the
indexes in place. Recorded in docs/graph/DECISION.md.
