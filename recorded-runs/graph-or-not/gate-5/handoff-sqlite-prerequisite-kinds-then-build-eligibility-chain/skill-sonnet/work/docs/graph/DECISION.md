# Graph decision

Decision: recursive-sql

Advising wants, on each course page, every course needed before taking it: required and concurrent prerequisites, followed all the way back, never through a recommended one, on a catalogue of 2,400 courses and 3,900 prerequisite rows. A recursive query on the SQLite file already in use fits. One trace can touch at most 2,400 courses and 3,900 rows, and `prerequisite_requires` and the primary key already index the walk.

## Workload facts

- Question asked of the connections: a walk from one course along "requires" links to a data-dependent depth, over the `prerequisite` table (db/schema.sql; the TODO in advising/pages.py). Today no query walks: sql/listed_prerequisites.sql lists the direct rows only.
- Counts: 2,400 courses, 3,900 prerequisite rows, longest chain 7 deep (stated by the user).
- Rule from the registrar: `required` and `concurrent` prerequisites both count (a concurrent one still has to be passed by the end of that term), `recommended` never counts, and neither does anything reached only through a recommended one; otherwise the whole chain, all the way back (stated by the user).
- Loops: cross-listed pairs list each other as required; Lin counted 23 of them and the registrar will not clean them up before next year (stated by the user). Each is a 2-cycle, so a walk has to deduplicate on course.
- Catalogue is a SQLite file of about 1.5 MB, rebuilt every term from the registrar's export by advising/importer.py (stated by the user; the importer deletes and recreates var/catalogue.db).
- Load: about 3,000 course page views a day (stated by the user) = 3,000 / 86,400 = about 0.035 per second, about 1 every 29 seconds on average. Peak rate unknown.
- Edges per course: 3,900 / 2,400 = about 1.6 on average (stated counts, divided). Tail fan-out and hubs: unknown.
- Bound on required work: a correct walk visits each course once, so at most 2,400 courses and 3,900 rows per page view (stated counts). The walk is also at most 7 levels deep (stated). `prerequisite_requires` indexes the column the walk enters by, and the primary key `(course_id, requires_id)` covers lookups by course_id (db/schema.sql).
- What is operated today: SQLite through sqlite3 in Python 3.12, queries as files in sql/ run by advising/db.py (README.md, advising/db.py). No other database, no dependency beyond the standard library.
- Writes and freshness: read-only between rebuilds; staleness is up to one term (stated by the user, rebuilt every term).
- Tried before: nothing recorded. The repo has no decision record, migration history or slow-query log.
- unknown: any timing (no var/catalogue.db in the repo, it is gitignored, so nothing was run or measured). Peak page-view rate. The number of courses with no prerequisites at all or the real size of the largest chain.

## Options considered

- graph-database (a dedicated graph store, as Adaeze proposes): rejected, because the whole data set is 1.5 MB and 3,900 rows, the walk is at most 7 deep, it is read-only between term rebuilds, and the load is about 0.035 views a second. A second stateful system and a load step after every rebuild buy nothing at this size.
- in-process-library (catalogue loaded into memory, for example a Python graph library): rejected, because it is not needed: SQLite already serves the walk from its indexes, and the repo uses the standard library only. It would fit in memory easily at 3,900 edges, so it is the fallback if the recursive query is measured too slow.
- recursive-sql (recursive queries on the SQLite catalogue already run): chosen, because the required work is bounded by 2,400 courses and 3,900 rows per view (above), at 0.035 views a second, over indexed columns. The query, described and not applied: start from the page's course; the recursive step follows `prerequisite` rows where `kind IN ('required', 'concurrent')` from `course_id` to `requires_id`, so `recommended` rows are never followed and anything reached only through one is never visited; use plain `UNION` on the course id with no depth or path column, so each course appears once and the 23 cross-listed loops end; exclude the starting course from the result; join `course` for the code and title. It would live in a new sql/ file called from advising/pages.py. How long it takes has not been measured (no database copy).
- no-graph (plain joins, no traversal): rejected, because the registrar asks for the whole chain, so the depth depends on the data. The existing one-step join in sql/listed_prerequisites.sql shows only direct rows.

## What would change the decision

- A measured p95 of the recursive query on a real `var/catalogue.db` above the page's latency budget (the advising web team sets that budget; none is stated) would move this to in-process-library, since 3,900 edges load in memory trivially at each term rebuild.
- Page views rising from 3,000 a day to a rate where concurrent traces strain SQLite, or the catalogue growing by orders of magnitude (many millions of rows), would reopen the question; neither is close at 1.5 MB.
- The registrar changing the rule so that, for example, "one of" alternatives or grade conditions must be evaluated would change the query, not necessarily the option; whole-catalogue analyses (every course's full chain for a degree audit) would favour in-process-library as a batch job.
