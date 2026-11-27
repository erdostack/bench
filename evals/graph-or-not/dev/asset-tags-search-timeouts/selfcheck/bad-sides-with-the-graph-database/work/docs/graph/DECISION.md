Decision: graph-database

## Workload facts
- Migration 0031 added `tag_implications`: 23,870 links, 11 levels deep, several broader terms per term.
- `expanded_tag_ids` returns 1,912,406 rows for 2,912 terms; 14.2% of searches are cancelled at 5 s.

## Options considered
- Recursive SQL: this is what is timing out. Relational databases are not built for hierarchies with
  shared sub-terms.
- Graph database: taxonomies are a native fit and traversals stay fast at any depth. Chosen.

## What would change the decision
- Operational cost.
