# Graph decision

Decision: recursive-sql

The question was whether to move the customer organisation hierarchy (2,300 organisations, up to 7 levels) into a graph database before the merger. What runs today already meets the need: the nightly rollup takes about 2 minutes against a 20-minute trigger, and the account-page subtree query is 12 ms p95 against a 150 ms trigger. The recursive queries on the SQLite file stay, and nothing needs changing.

## Workload facts

- Question asked of the connections: a walk down the parent relation to a data-dependent depth (accounts/subtree.py, `sub` recursive query from one root) and a walk up it for every organisation (rollups/rollup.py, `anc` recursive query), each a recursive query on the existing SQLite file.
- Size: 2,300 organisations, deepest group 7 levels (stated by the user).
- Nightly rollup takes about 2 minutes (stated by the user), inside a 30-minute batch window (stated by the user).
- Account-page subtree query: 12 ms p95 at about 40 page loads a minute (stated by the user) = 40 / 60 = about 0.67 queries a second.
- Agreed trigger for looking at storage again, set with ops: only if the nightly rollup goes past 20 minutes (it has to fit in the 30-minute batch window), or the account-page subtree query goes over 150 ms p95 (stated by the user).
- Headroom against those triggers: 20 min / 2 min = 10 times for the rollup, and 150 ms / 12 ms = 12.5 times for the subtree query (stated figures, divided). Neither trigger is met today.
- Shape of the data: `org.parent_id` is a single column, so each organisation has at most one parent and the hierarchy is a forest of trees, not a many-parent graph (db/schema.sql). `org_parent` indexes the column the subtree walk enters by (db/schema.sql).
- Required work: the rollup's ancestor table has one row per organisation per ancestor level, at most 2,300 x 8 = 18,400 rows (2,300 organisations times at most 7 levels plus the organisation itself, from the stated figures); it is joined to `invoice` on the indexed `invoice_org(org_id, issued_on)`. A tree walk visits each node once, so `UNION ALL` does not multiply rows in either query. Both carry a depth cap of 30 (accounts/subtree.py, rollups/rollup.py).
- What is operated today: one SQLite database `var/orgbook.db`, loaded from the CRM every evening, Python 3.11+ with no third-party packages (README.md).
- Freshness: the data is a nightly load, so a day-old answer is what the pages show today (README.md).
- Tried before: nothing recorded; there is no decision record, migration history or slow-query log in the repo beyond the user's account of the agreed triggers.
- unknown: how large the organisation count and the invoice count will be after the merger (no figure given and none in the repo). The number of invoices (the rollup's other input). I measured nothing: there is no copy of var/orgbook.db in the repo (gitignored), so these are the user's figures, not mine.

## Options considered

- graph-database (a dedicated graph store, as Bram proposes): rejected, because the approach in place meets both of the stated limits with 10 times and 12.5 times headroom. It would add a second stateful system, a CRM feed and a new query language to solve a problem the numbers do not show, and the merger's size is not stated.
- in-process-library (the edges loaded into memory, for example a Python graph library): rejected, because it is not needed: both queries meet their limits as written, and the repo is standard library only.
- recursive-sql (recursive queries on the SQLite file already run): chosen, because both measurements are well inside the agreed triggers (2 min against 20 min, 12 ms against 150 ms), and the data is a tree with an index on the walk column. The advice is to change nothing.
- no-graph (plain joins, no traversal): rejected, because both features walk the parent relation to a depth that depends on the data.

## What would change the decision

- The nightly rollup running past 20 minutes, the limit agreed with ops, would reopen the storage question. The first step would be to check whether the time is in the ancestor walk or in the `invoice` join, before moving the data anywhere.
- The account-page subtree query going over 150 ms p95, the limit agreed with ops, would do the same, again checking the plan first.
- The merged data set being known to be many times larger than 2,300 organisations (the headroom is about 10 times on the rollup) would be the time to re-measure on a copy of the merged data, before the numbers drift to the limits.
- Organisations that can have more than one parent (joint ventures, for example), so that `parent_id` no longer describes the structure, would change the shape of the walk and mean checking for route-per-row growth under `UNION ALL`.
