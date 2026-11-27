# Decision: tag search timeouts

Decision: no-graph

## Workload facts
- Tags are flat labels (ADR 004): `tags` and `asset_tags`, 7,340 tags and 31.6 million asset-tag rows.
- Tag search joins `asset_tags` to `assets`; the statement timeout is 5 s and 14.2% of searches hit it.

## Options considered
- Graph database: absurd for a join table. There is nothing to traverse.
- Add an index on `asset_tags (tag_id)`: chosen. A 31.6 million row table without the right index
  explains the timeouts on popular tags.

## What would change the decision
- If tags ever became hierarchical.
