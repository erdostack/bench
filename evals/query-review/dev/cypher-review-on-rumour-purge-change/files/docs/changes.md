# Changes

- One file per change, `db/changes/NNNN_name.cypher`, statements separated by `;`.
- `tools/apply.py` applies each file once, in order. Files are applied after the PR is merged.
- Live is read all day: a statement that changes more than 10,000 rows commits in batches of at most
  10,000 rows (`CALL { ... } IN TRANSACTIONS OF n ROWS`).
