Decision: recursive-sql (written up in docs/adr/0007-nested-groups-in-the-permission-check.md).

Stay on Postgres and make the check recursive. With 1.1M membership rows nested at most 6 deep, the walk from a user
up through its groups is a handful of index lookups; your hand-run CTE measured 9 ms p95 against a 50 ms budget, so
there is more than 5x headroom at 400 checks a second. That also satisfies your SRE lead's rule: the check does not
miss its budget on Postgres, so no new datastore. I would not bring the closure table back (40 minute rebuild against
a sync every 15 minutes), and an in-memory copy in every API node has the same staleness problem with more moving
parts.

The tripwire is written into the decision file: if the check misses 50 ms p95 on Postgres with the indexes in place,
the agreed move is to a dedicated graph store, not more workarounds.
