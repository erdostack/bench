# 0002 Neighbour letters

Date: 2026-11-23. Status: accepted.

Decision: recursive-sql

We stay on the existing Postgres/PostGIS database and join parcel_adjacency (written nightly by GIS). No recursion is
needed: the planning bylaw limits letters to the first ring, not neighbours of neighbours.

Numbers from the owner: 480k parcels; 2.7M adjacency rows; about 150 applications a week; one Monday batch; the
lookup takes 3 ms per application on the replica. The contractor's graph database pitch was turned down.
