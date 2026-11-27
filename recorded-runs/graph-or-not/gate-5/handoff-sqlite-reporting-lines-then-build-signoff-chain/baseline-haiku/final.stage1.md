Decision: recursive-sql

Keep the HR directory in the existing SQLite export and compute the sign-off chain with one recursive query. Neither a graph database nor an in-memory graph library is needed for this.

Why:
- The chain is a walk up the solid reporting line. The schema allows only one solid line per employee (`reporting_line_one_solid`), so each step is a single indexed lookup, and a chain is at most 12 steps. The approval page runs about 200 times a day, so the cost is negligible.
- The 3 MB export holds 6,400 employees and 7,900 reporting lines. A recursive query over that is well within what SQLite does per page view.
- The rules map directly onto the query. I tested the shape on a small sample with a grade-4 submitter's chain, a dotted-line lead, a loop, and a grade-7 submitter:
  - Only `kind = 'solid'` rows are followed, so a dotted-line lead never appears.
  - The chain stops after the first approver with grade 7 or above, and nobody between is skipped.
  - The path string includes the submitter, so a chain that returns to anyone already in it, including the submitter, stops there. The loop case returned only the one manager before the return to the submitter.
  - A submitter who is themselves grade 7 or above still gets the chain from their own manager, as the rule says.

The query shape:
- Seed with the submitter, carrying their id, grade and a path string such as `,id,`.
- Join the solid line of the current person, and the manager's grade.
- Recurse only while the current row is the submitter or has grade below 7. Skip any manager whose id is already in the path. Cap the depth at 12 as a guard.
- Return rows with depth above 0, ordered by depth. HR ops picks up any loop case by hand, so the page should show a note when the chain stops early on a loop.

Open points for Finance and HR:
- The 23 loops are in the HR export and should be reported to HR ops as they are found. The query stops at them but does not say why the chain ended; if the approval page should show that, it needs a second check for the loop case.
- The tests used a small hand-made sample, not the real export. Run the query against the hourly export before relying on it.

Why not the other options:
- graph-database: a second database to run and sync hourly for a 12-step walk, 200 times a day, is not justified.
- in-process-library: loading the org chart into memory and adding a graph dependency would break the project's standard-library-only setup, and the query does the job.
- no-graph: the problem is a walk up a chain of reporting lines, which is a traversal, even though it is short.
- need-more-information: the rules are settled and the data store does not change the answer.
