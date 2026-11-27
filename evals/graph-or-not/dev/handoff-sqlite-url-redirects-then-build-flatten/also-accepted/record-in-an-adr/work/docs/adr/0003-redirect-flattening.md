# 0003. Flattening redirect chains

Status: Accepted, 2026-11-23

Decision: recursive-sql

Facts from the owner: 1.9M redirects, longest chain 6 hops, 214 loops (renamed and renamed back). The nightly
job has 1 hour and takes 4 minutes. Agreed with SEO: URLs whose chain loops are left out of the map and fixed by
hand.

Options: Neo4j (Ravi) rejected, a second store for a nightly walk; an in-memory walk in the job would also work;
chosen a recursive query that carries the visited paths.
