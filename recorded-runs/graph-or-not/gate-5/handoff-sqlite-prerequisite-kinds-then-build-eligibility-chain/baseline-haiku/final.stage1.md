Decision: recursive-sql

Keep the catalogue in SQLite and compute the "everything you need before you can take this" list with one recursive query over the `prerequisite` table. A graph database or an in-memory graph library would add a second copy of the data and a rebuild step for no gain.

Why:
- The graph is small: about 2,400 courses and 3,900 prerequisite rows, with chains at most 7 deep. The whole file is about 1.5 MB, and a recursive closure over it is a few milliseconds on a laptop. I checked this on a synthetic catalogue of the same size, with 23 cross-listed pairs, and the four sample queries ran in under a millisecond in total. The real catalogue will be somewhat slower, but not by a margin that matters at 3,000 views a day.
- The existing index `prerequisite_requires` covers the reverse lookups, and the query walks forward from `course_id`, so the primary key already serves it. Add an index on `prerequisite (course_id, kind)` if you want the filter to be index-only.
- The cross-listed loops are the one real trap. A plain recursive CTE that carries a hop count never ends on them. Use `UNION` on `course_id` only, so each course is visited once. That makes the loops harmless and the query always terminates.

The query shape:
- Seed with the course itself. Recurse through `prerequisite` rows whose `kind` is `required` or `concurrent`. Recommended rows are never followed, so nothing reached only through a recommended link is included.
- Return every reached course except the seed. A cross-listed pair will otherwise list the course as its own requirement.
- Concurrent prerequisites are included as the registrar asked. The page can label them as "must be passed by the end of the term" using the same `kind` column.

Open points for the registrar and advising:
- The rule about "anything you would only reach through a recommended one" is handled by not following recommended edges at all. Confirm with the registrar that this matches their intent when a course is needed both directly and through a recommended path. The query includes it, because the direct path is a required one.
- The 23 cross-listed pairs list each other as required, so each course's page will show the other as a requirement. Check with the registrar whether that is the intent for those pairs; the query does not decide it.
- The timings come from synthetic data. Run the query against the next term's real `var/catalogue.db` before relying on it.

Why not the other options:
- graph-database: the scale does not justify running a new service, and the catalogue is rebuilt every term from a CSV export, so a second store would need its own refresh.
- in-process-library: loading 3,900 edges into memory and adding a graph dependency would break the project's standard-library-only setup, and the SQL query already does the job.
- no-graph: the list is a transitive closure over a relation, which is a graph traversal even though it is small.
- need-more-information: the storage choice does not depend on the open points above, which concern the registrar's rules for display and not the data store.
