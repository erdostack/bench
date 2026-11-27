Position: keep

Thanks for the suggestion. We looked at this when we built the letters and decided to keep it as a plain join on
parcel_adjacency in our Postgres database, the table your team already fills every night. The reasons are specific
to what the letters have to do:

- The bylaw requires letters to the first ring only: owners of parcels that share a boundary, never neighbours of
  neighbours. Multi-ring notification isn't something we may do, so it isn't something to prepare for.
- The lookup for one application takes 3 ms on the replica.
- We get about 150 applications a week and send the letters as one batch on Monday mornings.
- The data is 480k parcels and 2.7M adjacency rows, and it already lives next to the geometries in PostGIS.

A graph database would mean a second copy of that data, refreshed every night, for one join a week. If the bylaw
ever changes to more than one ring, a bounded recursive query on the same table covers it.
