Position: switch

Nadia is right. A recursive query with a hard cap of 3 links is bounded, Postgres handles that well with the
index on link(to_id), and it avoids keeping a second copy of the wiki in memory on every API host.
