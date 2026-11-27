# Changes

`db/changes/NNNN_what.cypher`, one change per file, reviewed, applied to prod by the release job
(auto-commit) after merge. Staging is a copy of prod restored every Monday; the release job applies
pending changes there first and fails the release if one times out (5 minutes).

Size: at most 100,000 deleted nodes per transaction. Larger deletes: CALL { } IN TRANSACTIONS.

Production runs Neo4j 2026.10.2.
