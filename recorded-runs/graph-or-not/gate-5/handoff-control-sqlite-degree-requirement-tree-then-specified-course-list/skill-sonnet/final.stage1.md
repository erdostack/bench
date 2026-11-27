Decision: recursive-sql

Do the "everything including sub-requirements" lookup with one recursive query on the SQLite database you already use. Neo4j is not warranted.

The numbers it turns on:
- 1,900 requirements and 14,000 listings in total, nesting at most 5 levels. A walk from any requirement cannot touch more than 1,900 requirements and 14,000 listing rows. The average programme is about 14 requirements and 100 listings (1,900 / 140 and 14,000 / 140).
- It is a verified tree: audit/importer.py refuses a catalogue where a requirement would end up inside itself, and each requirement has one parent_id.
- About 2,000 views a day in registration week (one every 43 seconds on average) and almost none otherwise, on data rebuilt once a term.
- `requirement_parent` and the primary key on `requirement_course` already index both steps of the walk.

How to do it (not applied): add a file in `sql/` with `WITH RECURSIVE sub(id) AS (SELECT :requirement_id UNION SELECT r.id FROM requirement r JOIN sub s ON r.parent_id = s.id) SELECT DISTINCT course_code FROM requirement_course WHERE requirement_id IN (SELECT id FROM sub) ORDER BY course_code;` and call it from `requirement_page` in audit/views.py. The DISTINCT matters because a course can be listed under several requirements.

What I could not find or measure:
- `var/audit.db` is not in the repo, so I ran nothing: no row counts, plans or timings. The size of the largest programme and the peak views per hour are unknown, but the whole-catalogue upper bound above already makes them irrelevant to the choice.

I would revisit this if a real run for the largest programme missed a latency budget you set (then load the tree in memory, or precompute the sub-requirement closure at import), or if the nesting stopped being a tree.

The decision is written to docs/graph/DECISION.md. Nothing else in the repo was changed.
