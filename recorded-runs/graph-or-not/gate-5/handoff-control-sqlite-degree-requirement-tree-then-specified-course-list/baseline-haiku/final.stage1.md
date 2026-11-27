Decision: recursive-sql

The question is a walk down a requirement tree: start at one requirement and collect the courses listed under it and under every sub-requirement below it. The tree is at most 5 levels deep, the catalogue is about 1,900 requirements and 14,000 course listings, and the page gets about 2,000 views a day at peak. That is a small query on a small table, and the existing SQLite database already has the indexes it needs.

The query, untested (there is no `var/audit.db` in the workspace):

    WITH RECURSIVE sub(requirement_id) AS (
      SELECT :requirement_id
      UNION
      SELECT r.id FROM requirement r JOIN sub s ON r.parent_id = s.requirement_id
    )
    SELECT DISTINCT rc.course_code
    FROM sub s JOIN requirement_course rc ON rc.requirement_id = s.requirement_id
    ORDER BY rc.course_code;

It can live in `sql/` as a new file beside `direct_courses.sql`, and `audit/views.py` can call it in place of the TODO. The existing `requirement_parent` index serves the recursive step, and the primary key on `requirement_course (requirement_id, course_code)` serves the join.

Why not the others:
- Neo4j: the graph is tiny, so a dedicated graph database gives no speed the audit needs. It would also mean a second system, kept in step with the importer that rebuilds `var/audit.db` each term, and that sync is a new failure point for a page that is quiet most of the year.
- In-process graph library: the catalogue would have to be loaded into memory and kept in sync with the importer, for a query the database already answers in milliseconds.
- No graph: the requirement is a tree, and the answer needs its descendants, so a traversal is required.

Points to get right:
- `DISTINCT` matters. A course can be listed under several requirements, so it could appear more than once in the rolled-up list. It should appear once.
- The `UNION` (not `UNION ALL`) is a guard. The importer refuses a catalogue that is not a tree, but the query should still terminate if the data is ever wrong.
- Decide whether the page shows which sub-requirement each course came from. That needs one more column and changes the output shape, so it should be settled before the TODO is closed.
- Nothing was run, and I did not change `audit/views.py`, since the request was for a decision.
