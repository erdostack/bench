I looked at SA-14 and my recommendation is to answer it as "not applicable, by design", not to change the job. The only edit I made is a comment above the statement that says why.

**Why the unscoped DELETE is correct here.** `reach` is not source data. It is the set of (ancestor, descendant) pairs that follows from `group_edges`, and `refresh_reach` is the only writer. The job empties it and refills it from `group_edges` with the next statement, both inside one `with conn:` transaction. So nothing is deleted that is not recomputed immediately, and because the database is in WAL mode the permission check keeps reading the previous closure until the commit. `docs/jobs.md` describes exactly this.

**Why the remediation in the finding would be a regression.**

- *Scope to groups whose `updated_at` changed*: this leaves wrong rows behind. When a group is taken out of another, `app/nesting.py` touches only the parent. But every ancestor of that parent loses its path to the child and to everything under the child, and none of those ancestors has a new `updated_at`. Their rows would stay in `reach`, and a stale row there is a permission that should have been revoked. I tried it on a copy: after removing 60 nestings, a refresh scoped that way leaves several hundred revoked pairs in place; the current job leaves none.
- *Batch it*: batches mean commits in between, and then the permission check can find `reach` empty or half filled. `docs/jobs.md` says that must never happen. The single transaction is about 4 s on production according to the same page.

**Suggested wording for the auditor:** "reach is a derived closure table with a single writer. The job replaces its whole content atomically (delete and re-insert in one transaction); no source data is deleted. Scoping or batching the delete would produce incorrect permission data. Documented in docs/jobs.md and in the job source."

Tests pass, behaviour unchanged.
