Decision: recursive-sql (option C in the ADR). Written to docs/adr/0007-zone-nesting-adr-0004.md.

The ADR's own measurements settle it: 2,400 zones nested at most 5 deep, 35 checks a second at shift change, and the
recursive walk up from the door's zone took 4 ms where the controllers allow 100 ms. Option A adds a database to run
for 2,400 rows. Option B would also work at this size but adds a cache to invalidate when facilities edit zones;
there is no latency problem for it to solve.
