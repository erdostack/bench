# Graph decision

Decision: in-process-library

The linked-accounts panel must return every account connected to the one being looked up through shared device ids or shared payment cards, at any chain length, in under 2 seconds. The answer is to build the account links in memory once per nightly copy with networkx (already installed) and look up the connected component, and not to adopt a graph database. The finding it turns on is size: 1.1M signal rows at most are about 0.6 GB in a networkx graph (measured on a synthetic graph of that size), for 200 lookups a day on data that is a nightly copy anyway.

## Workload facts

- 240k accounts, 1.1M signal rows, about 200 lookups a day by moderators; anything under 2 seconds is fine (stated by the user)
- Rule from trust and safety (Ayla): two accounts are linked only by a shared device id or a shared payment card; a shared IP never links them, not even together with something else (stated by the user)
- Need: the whole group of linked accounts, however long the chain; the current panel misses accounts in 31 of 400 groups, the ones chained more than 3 steps, compared with networkx `connected_components` on last week's copy (stated by the user)
- Question asked: a walk over the shared-signal relation between accounts to a depth that depends on the data (moderation/links.py `linked_accounts`, `max_depth=3` loop, one SQL statement per account visited)
- The current query joins `signal` to itself on `kind` and `value` for every `kind`, so it also links accounts through `ip` signals, which breaks the rule above (moderation/links.py, SQL has no filter on `kind`; db/schema.sql lists kinds `ip`, `device`, `card`)
- Data: SQLite `var/forum.db` on the moderation host, a nightly copy of production, with an index on `signal (kind, value)` (README.md, db/schema.sql). Answers are therefore at most a day old already.
- Edge count: signal rows of kinds device and card are at most 1.1M, the share that is ip is unknown, so the in-memory graph has at most 1.1M account-to-value edges
- Memory: a networkx graph of 240k account nodes and 1.1M edges to 900k value nodes took about 600 MB, about 550 bytes per edge, measured with tracemalloc on a random synthetic graph (python3 with networkx 3.7); the shape of real data differs, so treat it as a sizing figure
- Load: 200 lookups a day is about 1 every 2 minutes in an 8-hour day (200 / 480 minutes = 0.4 per minute); the graph is rebuilt once after each nightly copy and the lookups read it (arithmetic from the stated figures)
- Operated today: Python 3.12, SQLite, networkx 3.7 for the dashboard charts (README.md, requirements.txt)
- unknown: the size of the largest group and the number of accounts that share a device or a card with hundreds of others (public machines and shared cards); there is no data copy in the repo and nothing was measured on the real data
- unknown: the memory of the moderation host and the number of processes serving the panel (looked in README.md and the repo; neither is stated)
- unknown: the time to build the graph from the real 1.1M rows; the synthetic build took 45 s under tracemalloc, which is much slower than normal, so it is only an upper bound
- unknown: whether the panel needs to see links by banned status or date; the request states none

## Options considered

- graph-database (a dedicated store such as the one Bilal proposes): rejected, because 1.1M rows and 200 lookups a day on a nightly copy fit in one process (about 0.6 GB), and a graph database would add a second store fed from the copy with no latency or size problem to solve.
- in-process-library (networkx, already installed): chosen, because the edges fit in memory, a nightly rebuild meets the freshness the nightly copy already has, and `connected_components` on last week's copy already gave the right groups, which shows it computes what the rule needs. Build the graph from `signal` rows where `kind IN ('device', 'card')` only, and look up the component of the account.
- recursive-sql (recursive query on SQLite): rejected, because it is not shown to hold: nobody has measured one on the real data, the size of the largest group is unknown, and shared devices and cards can make groups large. It remains possible, and would be a smaller change if a measurement on the real copy answers well within 2 seconds.
- no-graph (plain joins): rejected, because a join crosses the signal table a fixed number of times, and the groups that are missed are the ones chained more than 3 steps.

## What would change the decision

- A measurement on last week's copy showing a recursive query (one statement, `UNION` on account ids, `kind IN ('device','card')`) that answers the lookups for the largest group in under 2 seconds would move this to recursive-sql, which is the cheaper rung (the moderation team to run it).
- The graph build taking longer than the nightly window allows, or the host having too little memory for about 0.6 GB per process times the processes that serve the panel, would move this to recursive-sql or to a precomputed component id column.
- Signals needed live rather than as of the nightly copy, with the edge count growing by a factor of 50 or more (about 55M signal rows), would call for re-measuring and could move this to graph-database.
- Trust and safety changing the rule so that an IP can link accounts in some cases would change the edge filter, not the choice.
