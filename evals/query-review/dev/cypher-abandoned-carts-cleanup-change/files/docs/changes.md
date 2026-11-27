# Changes

One change per file, `db/changes/NNNN_what.cypher`, reviewed, applied by the release job after
merge as an auto-commit query.

Size: at most 50,000 deleted nodes, or 200,000 changed properties, per transaction. The delete of
old sessions in 0377 was one transaction of 9 million nodes; it filled the heap on all three members
and production was down for 40 minutes.
