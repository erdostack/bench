Decision: recursive-sql

Keep the customer hierarchy in the existing SQLite database and keep the recursive queries in `accounts/subtree.py` and `rollups/rollup.py`. A graph database is not worth moving to now.

Why:
- The storage review trigger that ops agreed is not met. The nightly rollup takes about 2 minutes against a 20-minute limit, and the account-page subtree query is 12 ms p95 against a 150 ms limit. Both are well inside the thresholds, so there is no evidence that the storage choice is the problem.
- The hierarchy is small: 2,300 organisations, at most 7 levels deep. Both queries walk `org.parent_id`, which already has an index (`org_parent`), and the rollup reads invoices through `invoice_org (org_id, issued_on)`.
- A graph database would add a second store to load from the CRM every evening, and the merger work does not change the shape of the data. The benefit does not justify that cost.
- The existing queries already guard against loops (`depth < 30`), so a loop in the CRM data cannot make them run away.

What I checked:
- I read the schema, both queries and the rollup job. I did not run them against the real `var/orgbook.db`, which is not in the working directory, so the 2-minute and 12 ms figures are the ones you gave me.
- I tried a synthetic run of the rollup with 300,000 invoices. It stopped with a datatype error I did not have time to track down, so I have no timing from it. The subtree query on synthetic data ran in well under a millisecond.

Open points:
- The rollup at 2 minutes for 2,300 organisations is slower than I would expect from this design. The ancestor table has only a few thousand rows, so the time is more likely to come from invoice volume or the query plan than from the hierarchy. Run `EXPLAIN QUERY PLAN` on `ROLLUP_SQL` and check the invoice row count. That is a query-tuning question, not a reason to change storage.
- Keep watching the rollup time against the 20-minute limit as invoice volume grows, since that is the limit that would reopen the storage question.

Why not the other options:
- graph-database: the agreed triggers are not met and the data is too small to need one.
- in-process-library: loading the hierarchy into memory for two queries that already take milliseconds adds a dependency and a load step with no gain.
- no-graph: the work is a traversal (subtree and ancestor walks), so it is a graph problem even though the data is small.
- need-more-information: the measured numbers and the agreed thresholds are enough to decide. The open item is about the rollup query plan, which does not change the storage choice.
