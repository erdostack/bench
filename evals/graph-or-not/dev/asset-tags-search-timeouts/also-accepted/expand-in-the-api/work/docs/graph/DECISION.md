# Decision: tag search

Decision: in-process-library

## What the repo shows

- `tag_implications` (migration 0031) holds 23,870 broader/narrower links between 7,340 tags, 11 levels
  at the deepest. So tags are a hierarchy with shared sub-terms, not flat labels.
- Search expands the term with the SQL function `expanded_tag_ids`. In the DBA's plan it produces
  1,912,406 rows for 2,912 distinct terms and takes about 9 seconds; the statement timeout is 5 s.
- `asset_tags_tag_id_idx` exists and is used. There is no missing index.
- 14.2% of searches were cancelled in week 46.

## Options considered

- Graph database: no. 23,870 rows, a dozen edits a week.
- Fix the SQL function so it does not repeat terms: fine as well.
- Load the 23,870 links into the API at start-up, refresh when a curator saves, and expand a term in
  memory with a visited set; then pass the list of tag ids to the existing indexed query. Chosen: the
  expansion becomes microseconds and is easy to test.

## What would change the decision

- More than one service needing the expansion: then do it in the database so they share it.
