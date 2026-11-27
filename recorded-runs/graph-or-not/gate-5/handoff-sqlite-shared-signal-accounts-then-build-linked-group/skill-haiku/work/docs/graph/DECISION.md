# Graph decision

Decision: in-process-library

The linked-accounts panel must return every account connected to a given account through shared device ids and payment cards only, at any depth, in under 2 s, for about 200 lookups a day over 240k accounts and 1.1M signal rows. That is a connected-component walk over a small data set, which networkx (already installed for the dashboard) computes from a copy loaded once per process and refreshed with the nightly copy; the walk must filter out IP signals, which the trust and safety rule forbids as links. The finding it turns on is size: 1.1M signal rows fit comfortably in one process, so the choice does not depend on how large the connected groups are. The current code also links accounts by shared IP, because its join has no kind filter, so the fix removes IP links as well as adding depth.

## Workload facts

- 240k accounts and 1.1M signal rows (stated by the user). Average about 4.6 signal rows per account (derived: 1.1M / 240k). The share of device and card rows is unknown.
- About 200 moderator lookups a day, and anything under 2 s is acceptable (stated by the user).
- The rule: two accounts are linked only by a shared device id or a shared payment card; a shared IP never links them, not even together with something else (stated by the user, from Trust and Safety, Ayla).
- Signal kinds are `ip`, `device` and `card`, with a primary key on `(account_id, kind, value)` and an index on `(kind, value)` (`db/schema.sql`).
- The current `linked_accounts` in `moderation/links.py` matches on `kind` and `value` with no kind filter, so it links accounts through shared IPs, which the rule forbids (derived by reading the query). It also stops at `max_depth=3`, which is the cause of the 31 of 400 groups the user found missing (stated by the user).
- The comparison reference, networkx `connected_components` on last week's copy, is not stated to exclude IP edges. If it included them, the 31 of 400 figure is measured against the wrong rule and must be recomputed (unknown).
- The panel is a TODO in `moderation/panel.py` pending this decision.
- Freshness: `var/forum.db` is a nightly copy of production (`README.md`). A panel built on that copy is as fresh as the copy, and a reload at each copy meets the freshness it already has (derived).
- Stack: Python 3.12, SQLite, networkx 3.7 (`README.md`, `requirements.txt`).
- Memory and load time for the device and card graph in networkx were not measured; no copy of `var/forum.db` is in the repo.
- unknown: the device and card share of the 1.1M rows; the size distribution of connected groups; the fan-out of the largest device or card value; whether the 400-group reference excluded IP edges; the time for the slowest lookup on the real copy.

## Options considered

- graph-database (Bilal's proposal, unnamed product): rejected, because the data is small (240k accounts, 1.1M rows), the load is about 200 lookups a day, and freshness is nightly anyway. A second server, a sync feed and a second copy of the signals cost more than a 2 s lookup over a file that already exists. The rule is a kind filter and a walk, not a feature a graph database would add.
- in-process-library (networkx, already installed): chosen. The data fits by arithmetic (1.1M rows), so the walk holds at any group size. Load the device and card rows once per process from the nightly copy, build the graph, and take each account's connected component. The load and walk time were not measured, so cache the graph per process and do not rebuild it per lookup.
- recursive-sql (one recursive query on `signal`, with `UNION` so each account is visited once and a device or card filter): passed over. It is the cheaper option, with no load step, and the existing indexes serve its joins. But its time per lookup depends on group and hub sizes that the repo does not record, and it has not been run on the nightly copy, so it is not shown to meet 2 s.
- no-graph (plain joins): rejected, because the linked set is a connected component of unbounded depth; the 31 groups chained beyond three steps show the depth is data-dependent.

## What would change the decision

- A recursive query with a device and card filter, using `UNION`, run on the nightly copy, returns every lookup under 2 s, including the slowest group: recursive-sql moves ahead, since it needs no load step or cache.
- Moderators need the panel on live data rather than the nightly copy: the in-process cache would then be stale, and recursive-sql on the live database becomes the candidate.
- Lookups grow to thousands a day across the forum, or links are needed across many more signal kinds at several hops: that is the point to test a graph database against the real query mix.
- The reference used for the 31 of 400 groups is shown to have included IP edges: then the missing-account count must be recomputed under the rule before any figure is reported.
