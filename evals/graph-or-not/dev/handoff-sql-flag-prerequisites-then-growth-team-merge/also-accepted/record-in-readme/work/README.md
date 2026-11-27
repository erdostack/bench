# flagship

Feature flags. The admin service stores flags in Postgres (`db/schema.sql`) and publishes a JSON snapshot
(`admin/snapshot.py`); every SDK downloads it and evaluates flags locally (`sdk/evaluate.js`).

## Decision: flag prerequisites

Decision: in-process-library

Evaluate in the SDK while the snapshot is under 5 MB and evaluation under 1 ms p99 (640 flags, 1,100 links, 1.2 MB, 0.08 ms today); past either, move evaluation server-side.
