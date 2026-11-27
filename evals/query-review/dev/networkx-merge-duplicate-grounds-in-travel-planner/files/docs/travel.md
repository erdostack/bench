# Travel data

- A leg joins two different grounds; `km` is the road distance and `origin` says where it came from:
  `survey` (measured by the league's volunteers) or `feed` (estimated by a fixtures feed).
- When the two fixture feeds were merged in October 2026, some grounds came in twice under slightly
  different names. `data/ground_merges.csv` lists each duplicate and the record to keep.
- Merging a duplicate into the record we keep: the kept record's name, town and legs stay as they are
  (they are the surveyed ones); the duplicate adds only legs to grounds the kept record has no leg to.
  The feed also added a short `same site` leg between some duplicates and their kept record; after the
  merge that would be a leg from a ground to itself, which the planner's leg counts and distance table
  do not allow.
