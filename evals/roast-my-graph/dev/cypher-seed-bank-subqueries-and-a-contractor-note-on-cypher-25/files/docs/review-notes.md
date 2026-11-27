# External review, 2026-11-14

1. HIGH: queries/accessions.cypher uses `CALL (b) { ... }` and `CALL (t) { ... }`. This is Cypher 25
   syntax and is not available on a 5.x server. These queries will fail. Rewrite every subquery with
   `CALL { WITH b ... }`.
2. LOW: consider APOC for the drawer report.
