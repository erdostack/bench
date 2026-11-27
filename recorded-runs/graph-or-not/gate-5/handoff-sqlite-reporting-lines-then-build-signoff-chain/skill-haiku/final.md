I added `signoff_chain(conn, employee_id)` to `hr/approvals.py`. It returns the ids of the approvers for a claim, in order, starting with the submitter's solid-line manager. The submitter is never in the list. Nothing else in the repo was changed, and `docs/graph/DECISION.md` was left as it was.

How it walks:
- It follows only `solid` reporting lines. Dotted lines are ignored.
- It stops after the first approver at grade 7 or above, and that approver is included as the last entry.
- It stops at a depth of 12 levels.
- It stops before a manager who is already in the chain, including the submitter. That person is not listed.
- A submitter with no solid line gets an empty list.

It is a recursive SQL query on the existing HR export, following the recorded decision (recursive-sql). The constants `SIGNOFF_STOP_GRADE = 7` and `SIGNOFF_MAX_DEPTH = 12` sit at the top of the module.

I checked it on an in-memory copy of `db/schema.sql` with small hand-made directories. A normal chain stops at grade 7. A dotted line is skipped. A two-person loop returns the one manager before the loop. A missing solid line returns an empty list. A long chain is cut at 12. I did not run it on the real export, which is not in the repo.

Open points for you:
- A list cut short by a loop, a missing line or the depth cap looks the same as a complete chain. The approval page cannot tell that a claim should go to HR ops by hand. The decision record suggests the query should report which ending it hit. I did not add that, because the request asked for just the function and the return shape is yours to choose.
- The record does not say whether the 12-level cap counts approvers or reporting lines. I counted approvers.
- The record also does not say how many employees have no solid line at the top of the organisation. Those return an empty list and need no special handling here.
