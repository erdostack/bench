Added sql/equivalents.sql, following docs/graph/DECISION.md.

- Pairs with status approved or provisional count; withdrawn never does (the registrar's rule in the record).
- Each pair is read in both directions, since it is stored once either way round.
- Equivalence is transitive with no limit, so it is a recursive walk; reading pairs both ways makes loops
  everywhere, so each walk carries the courses it has visited and never goes back to one.
- Returns (course_id, links) with the fewest links, without the course itself.

Tested on a small SQLite db with a ring of four courses, a withdrawn pair and a provisional one.
