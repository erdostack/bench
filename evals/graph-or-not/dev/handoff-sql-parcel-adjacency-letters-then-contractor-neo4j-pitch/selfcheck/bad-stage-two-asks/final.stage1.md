Decision: no-graph

The neighbours are already computed: parcel_adjacency has a row for every pair of touching parcels, written by the
GIS team each night. The bylaw only asks for the first ring, so the letters are one join (application -> parcel ->
parcel_adjacency -> parcel -> owner), and you measured it at 3 ms per application. At about 150 applications a week
in a single Monday batch that is under a second of database time a week. A graph database would mean copying 480k
parcels and 2.7M adjacency rows out of PostGIS every night to answer the same join. Written down in
docs/graph/DECISION.md.
