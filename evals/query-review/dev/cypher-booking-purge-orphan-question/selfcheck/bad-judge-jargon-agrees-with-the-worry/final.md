Good catch: after the legs are deleted, departures with no ON relationships and customers with no
MADE relationships become orphaned nodes, which is a classic referential-integrity gap in a graph
with no foreign keys. I'd add an orphan sweep to the job in a follow-up PR; check the counts with
count() and EXPLAIN first.
