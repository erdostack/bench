# Changes

`db/changes/NNNN_what.cypher`, one change per file, reviewed, applied by the release job as an
auto-commit query after merge.

Size: a change that touches more than about 200,000 nodes, relationships or properties must be
batched with `CALL { } IN TRANSACTIONS` (see 0091). Smaller changes run as one transaction.
