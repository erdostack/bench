# Graph decision

Decision: recursive-sql

Advisors want every course that counts toward a requirement, including everything in its sub-requirements (the TODO in audit/views.py), and Kemal proposes loading the catalogue into Neo4j. Do it on the SQLite database already used with one recursive query down requirement.parent_id: the whole catalogue is 1,900 requirements and 14,000 listings, so a walk from any requirement can touch at most 1,900 requirements and 14,000 listing rows, and the page gets about 2,000 views a day.

## Workload facts

- Requirements: 1,900 across 140 programmes (stated by the user).
- Course listings: 14,000 (stated by the user).
- Nesting: at most 5 levels (stated by the user). The README and audit/importer.py enforce a tree: `check_tree` refuses a catalogue in which a requirement would end up inside itself, and db/schema.sql gives each requirement one nullable parent_id, so there is one route from a requirement to the top and no multiple paths.
- Load: about 2,000 views a day in registration week and almost nothing otherwise (stated by the user); about 2,000 / 86,400 s is one view every 43 seconds on average (derived), and registration-week peaks within a day are not stated.
- Writes and freshness: the database is rebuilt each term by audit/importer.py from the programme catalogue (README.md), so it is read-only between rebuilds.
- The question asked of the connections: from one requirement, go down parent_id to every sub-requirement at any depth up to 5, and collect the courses listed under the requirement and under each sub-requirement (a data-dependent walk along requirement.parent_id, then requirement_course). Today sql/direct_courses.sql returns only the direct listings.
- Indexes: requirement_parent on requirement(parent_id) (db/schema.sql) is the column the downward walk enters by, and requirement_course has PRIMARY KEY (requirement_id, course_code), so the listings of each requirement are found by index.
- Upper bound on required work: a walk from the top of the largest programme touches at most all 1,900 requirements, and 14,000 listing rows; per programme the average is 1,900 / 140 = about 13.6 requirements and 14,000 / 140 = 100 listings (derived, uneven programmes will be larger). Small against 2,000 calls a day.
- A course can be listed under several requirements (db/schema.sql comment), so the same course can be reached by more than one sub-requirement; the result needs DISTINCT course_code.
- Engine and tooling: Python 3.12, SQLite `var/audit.db`, queries are files in sql/ with :named parameters (README.md); the db file is not in the repo.
- unknown: size of the largest programme's tree and the peak views per hour in registration week, no data in the repo. They do not change the decision, because the whole catalogue is the upper bound above.
- Nothing was run: var/audit.db is not in the repo, so no row counts, plans or timings were taken.

## Options considered

- graph-database (Neo4j, as Kemal proposes): rejected, because the tree is 1,900 requirements deep at most 5, rebuilt once a term and read about 2,000 times a day; a second stateful system and a feed from the catalogue would be added for a walk that touches at most 1,900 requirements. "Requirement trees are graphs" describes the shape of the data, not a workload that needs one.
- in-process-library (the edges loaded into memory): rejected, because it is not needed; the data is already in SQLite, a recursive query does the same walk without a second copy to load and refresh each term.
- recursive-sql (a recursive CTE on the SQLite database already used): chosen, because the walk starts from one requirement, the nesting is a verified tree of at most 5 levels, requirement_parent and the primary key on requirement_course already index both steps, and the required set is small. Suggested shape (not applied; nothing in the repo besides this file was changed): add a file sql/counting_courses.sql with `WITH RECURSIVE sub(id) AS (SELECT :requirement_id UNION SELECT r.id FROM requirement r JOIN sub s ON r.parent_id = s.id) SELECT DISTINCT course_code FROM requirement_course WHERE requirement_id IN (SELECT id FROM sub) ORDER BY course_code;` and call it from requirement_page next to the direct list. SQLite supports recursive CTEs, and because the data is a tree, UNION is enough to deduplicate.
- no-graph (plain joins, no traversal): rejected, because the walk follows parent_id for a depth that depends on the data (up to 5 levels); a fixed number of self-joins would work for 5 levels but would break if the limit grew, and it is the same walk written out by hand.

## What would change the decision

- A run on the real var/audit.db where the recursive query for the largest programme takes longer than the page's latency budget (the registrar's office or the platform owner sets that; none is stated): this would move it to in-process-library, a tree of 1,900 requirements loaded per process, or to precomputing the sub-requirement closure at import time.
- Peak concurrency in registration week far above what SQLite handles for read-only queries on a file of this size, measured as slow or failing requests with their total calls: ask for the peak views per hour.
- The nesting no longer being a tree (a requirement with more than one parent, which the importer's check_tree currently refuses) or depth growing far beyond 5: re-check the arithmetic and the query's deduplication.
- A new need for whole-catalogue analysis (for example which courses count toward the most programmes) would move that job to in-process-library, not the page.
