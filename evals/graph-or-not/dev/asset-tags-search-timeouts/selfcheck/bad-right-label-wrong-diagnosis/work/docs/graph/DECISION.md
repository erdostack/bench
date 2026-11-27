Decision: recursive-sql

## Workload facts
- 7,340 tags, 31.6 million asset_tags rows, statement timeout 5 s.
- 8,720 of 61,400 searches were cancelled in week 46.

## Options considered
- Graph database: not needed for tags.
- Stay on PostgreSQL and add the missing index on asset_tags: chosen.

## What would change the decision
- Timeouts continuing after the index.
