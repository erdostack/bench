Decision: recursive-sql

Keep the directory in its SQLite export and walk the solid reporting chain with a recursive query. Every employee has at most one solid manager, enforced by a unique index, so the chain is a single path of at most 12 steps. On a synthetic directory of the stated size, the query matched an independent walk for all 6,400 employees, and a walk took a median of 0.014 ms. A graph database would add a second system kept in step with an hourly export for a load of about 0.0023 page opens a second.

The query must do four things: follow only solid lines, stop at the first employee of grade 7 or above, stop before any manager already in the chain (including the submitter), and cap at 12 levels. It should also report why the chain ended (grade 7 approver, loop, missing line or depth cap), so HR ops can see which claims to pick up by hand.

Not known: how many employees have no solid line (the top of the organisation is not identifiable from the counts), whether the 12-level cap counts approvers or lines, the mix of two-person loops against longer cycles among the 23, and the page's latency budget. The timings come from synthetic data, not the HR export, so run the query on the real export before release.

Nothing in the repo was changed except the new file docs/graph/DECISION.md.
