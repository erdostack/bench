# Decision: is tag search a missing index or a graph database problem?

Decision: recursive-sql

Neither of you, though you are closer on the remedy: this stays in PostgreSQL. The diagnosis is wrong
on both sides.

## Workload facts

- Tags have not been flat since March. Migration 0031 imported the archive thesaurus into
  `tag_implications`: 23,870 broader/narrower links between the 7,340 tags, up to 11 levels deep, and a
  term can sit under several broader terms. ADR 004, the README and the data-model page predate it.
- Tag search (`src/search/byTag.ts`) calls `expanded_tag_ids`, a recursive query that walks from the
  searched term down through every narrower term. It uses UNION ALL, so a term that can be reached by
  several routes is returned once per route.
- Odile's plan for "Architecture" (`ops/explain-search-412.txt`): the function returns 1,912,406 rows
  for 2,912 distinct terms, and that step is about 9 of the 9.6 seconds.
- The index is not missing. `asset_tags_tag_id_idx` was added in migration 0012 and the plan uses it:
  13 rows per term, microseconds each.
- Week 46: 8,720 of 61,400 tag searches (14.2%) were cancelled at the 5 second statement timeout. For
  terms with six to eight levels below them it is 82%, for nine or more 97%. Leaf terms are fine.
- The thesaurus changes about a dozen times a week, by three curators.

## Options considered

- Add an index on `asset_tags` (your plan): it already exists, and the time is not spent there.
- A graph database (Lena's plan): the thing being walked is 23,870 rows that change twelve times a week.
  A second datastore and a sync for that is out of proportion, and the search still has to join to
  4.1 million assets in PostgreSQL afterwards.
- Expand the term in the API process from a cached copy of the 23,870 links: workable, and a fair
  second choice.
- Keep the walk in PostgreSQL and make it visit each term once: chosen. The walk is real (so this is not
  "plain tags"), it is small, and the database already holds everything it needs.

## What would change the decision

- The thesaurus growing by a few orders of magnitude, or needing questions SQL handles badly (shortest
  route between two terms across the whole vocabulary, say).
- The corrected walk still being slow on the broadest terms; then precompute each term's narrower set
  when a curator saves a change.
