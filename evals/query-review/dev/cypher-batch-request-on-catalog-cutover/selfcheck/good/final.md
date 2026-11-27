I'd leave 0093 as one transaction. Batching would make it less safe, not more.

- Size: it deletes and recreates 2,430 SERVES_FROM relationships and moves one label, about 4,900
  changes. docs/changes.md only asks for batching above about 200,000.
- It has to be atomic: docs/catalog.md says every store must have exactly one SERVES_FROM and exactly
  one catalog must be Live at any moment, and the app errors otherwise. In batches, each batch
  commits on its own, so stores would be split between two catalogs while it runs, and stuck that
  way if it failed halfway. 0085 and 0089 ran the same way.

To check before merging: `EXPLAIN` it, and afterwards
`MATCH (s:Store) WHERE COUNT { (s)-[:SERVES_FROM]->() } <> 1 RETURN count(s)` should be 0.
