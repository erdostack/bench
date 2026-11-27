Decision: recursive-sql

Flatten the chains with one recursive query on the replica and keep the job as it is. ADR: docs/adr/0003-redirect-flattening.md.

The table is 1.9M rows, chains are at most 6 hops, and the job has an hour of which it uses 4 minutes. The loops
(214 of them) are the thing to get right: the query carries the paths it has seen and stops when one comes round
again, and those URLs are left out of the map, as agreed with SEO. A graph database would be a second copy of the
table to keep in sync for a nightly batch.
