# Graph decision

Decision: recursive-sql

Advising wants the full "everything you need before you can take this" list on course pages, counting required and concurrent prerequisites all the way back and ignoring recommended ones; Adaeze proposes a graph database for it. The answer is a recursive query on the SQLite catalogue the course pages already read, because the walk is short, the table is small and indexed, and a measured full-reach walk takes milliseconds. The finding it turns on: 3,900 prerequisite rows at about 3,000 page views a day is a load of roughly 0.035 walks a second.

## Workload facts

- Courses: 2,400 (stated by the user).
- Prerequisite rows: 3,900 (stated by the user); 3,900 / 2,400 = 1.63 rows per course, so average out-degree is about 1.6 (derived from the two stated counts).
- Longest chain: 7 deep (stated by the user). The walk depth is data-dependent, so the query must follow the data rather than a fixed depth.
- Cross-listed pairs: 23, each listing the other as required (stated by the user; Lin counted); the registrar will not remove them before next year (stated by the user). If each pair is two rows, that is 46 of 3,900 rows, 1.2 percent (derived; the export itself is not in the repo).
- Kinds of prerequisite row: `required`, `concurrent`, `recommended` (`db/schema.sql`, comment on `prerequisite`). The rule stated by the registrar: required and concurrent count, a concurrent prerequisite counts for the whole chain behind it, recommended never counts, and nothing reached only through a recommended edge counts (stated by the user).
- Size of the catalogue: about 1.5 MB, rebuilt each term by `advising/importer.py` into `var/catalogue.db` (stated by the user; `README.md`; the file is not in the repo, `.gitignore`).
- Load: about 3,000 course-page views a day (stated by the user) = 3,000 / 86,400 = 0.035 views a second on average; peak rate unknown. Each view runs one walk if the list is not cached.
- What runs today: `sql/course.sql` and `sql/listed_prerequisites.sql` read one course and its direct edges with no traversal (repo files). The list the TODO asks for is a new walk, not something the code does now.
- Indexes in place: the primary key `(course_id, requires_id)` gives the forward walk an index on `course_id`; `prerequisite_requires` on `requires_id` (`db/schema.sql`).
- Measured, correctness and cycles: a synthetic catalogue of 2,400 courses, 3,233 prerequisite rows (2,274 required, 173 concurrent, 786 recommended), a 7-level layered structure, and 23 mutual required pairs, in SQLite 3.53.1 under Python 3.13. The recursive query, with `UNION` on the course id only and a filter on `kind` in the recursive step, matched an independent breadth-first search for all 2,400 courses, and terminated on the mutual pairs (scratch run in this task, command not kept). The synthetic is not the registrar's data.
- Measured, timing for the typical walk: on the same synthetic catalogue, median 0.01 ms, p99 0.05 ms, maximum 8.1 ms per course; the query plan shows `SEARCH prerequisite USING INDEX ... (course_id=?)` inside the recursive step.
- Measured, worst case: a synthetic in which one course reaches all 2,399 others through 3,900 rows, in memory: median 13.25 ms, maximum 34.28 ms over 20 runs. This is a bound, since the real chain is 7 deep.
- Arithmetic: the closure of any course is at most 2,399 courses and a walk reads at most 3,900 rows. At 0.035 walks a second and a worst case of 0.034 s each, the database spends about 0.12 percent of one core on this, so the load is negligible.
- Synthetic file size was 299 KB; the registrar's file is about 1.5 MB, so the synthetic is not a size match and is used only for timing and correctness.
- unknown: the real share of `recommended` rows (the synthetic used 25 percent, which is a guess and not used in the decision); the peak view rate; whether each cross-listed pair is exactly two rows; whether the page should count the course itself when a loop returns to it (the query excludes it, which is the reading that makes the list make sense); the latency budget for a course page (not stated); whether the catalogue has more rows than the 3,900 stated. Looked in: `README.md`, `db/schema.sql`, `sql/course.sql`, `sql/listed_prerequisites.sql`, `advising/db.py`, `advising/importer.py`, `advising/pages.py`, `.gitignore`. `var/catalogue.db` was not present.

## Options considered

- graph-database (a dedicated graph store, as Adaeze proposes; no product named in the request): rejected, because the longest chain is 7 deep, the walk runs over 3,900 rows, and the worst measured walk is 34 ms on the synthetic. Adopting one would add a second stateful system and an import step from the registrar's export for a load of about 0.035 walks a second.
- in-process-library (the edges loaded into memory): not chosen. It would fit (1.5 MB file), but it adds a loader and a copy per web process that must be reloaded each term; the recursive query on the existing file meets the need without that.
- recursive-sql (recursive queries on the database already run): chosen, because the walk starts from one course, SQLite is already the store, the primary key and the `requires_id` index serve the walk, and the measured walks are well inside any page budget. The query must carry the `kind` filter into the recursive step, use `UNION` on the course id (not on a hop count), and exclude the starting course from its own result, which handles the 23 loops. This is the fix to run on the real catalogue before release.
- no-graph (plain joins, no traversal): rejected, because the list needs every course reachable through required and concurrent edges, to a depth of up to 7 that the data sets; one join cannot reach that.

## What would change the decision

- The p99 time of the list query on the real catalogue (measured with the `kind` filter and the loop guard in place) exceeding the page latency budget that the advising owner sets would move this to in-process-library, with the closure precomputed at import each term.
- A peak view rate far above the 0.035 a second average, sustained at a level where the summed walk time approaches one core of the web database, would move this to precomputing the lists at import (still recursive-sql, batch) and only then to in-process-library.
- A requirement to walk across catalogues or terms, beyond the single export, that makes the set too large for one database file would move this to graph-database; the advising owner and the registrar set that scope.
- A change in what counts (for example, counting recommended rows or cross-listed rows as one course) changes the query, not the choice; it is not a condition to move options.
