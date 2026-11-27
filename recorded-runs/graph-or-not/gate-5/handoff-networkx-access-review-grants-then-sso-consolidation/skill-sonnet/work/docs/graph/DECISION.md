# Graph decision

Decision: graph-database

The question was whether the nightly access review (review/reach.py: who can reach payroll, treasury and so on through nested groups and grants) still stays on networkx in memory on review-01. It does not: after the SSO consolidation the job peaked at 3.1 GB on two nights running and was OOM-killed both times, against the 2 GB of the certified review-01. The CISO's rule sends the job to the graph database on the certified security cluster once it no longer fits, and a bigger box is off the table. Previous decision, kept here for the record: in-process-library, on a peak of about 260 MB.

## Workload facts

- Question asked of the connections: for each of 4 sensitive systems, all identities that reach it by walking edges backwards through identity to group, group to group and group to system, depth set by the data (`nx.ancestors`, review/reach.py; edge direction in review/load.py). Unchanged since the earlier decision: a walk of unknown depth, so not no-graph.
- Size, now against before (stated by the user): 410,000 identities (was 38,000, 10.8 times), 52,000 groups (was 6,500, 8 times), 4.6 million membership edges (was 390,000, 11.8 times). These come from the SSO consolidation; the subsidiaries' directories are now in the export.
- Peak memory, now against before (stated by the user): 3.1 GB (was about 260 MB, 12.2 times). The job was OOM-killed on review-01 the last two nights. 3.1 GB = 3,174 MB against the 2,048 MB limit, which is 1.55 times the limit. The 3.1 GB is the peak the user reported; the true need of an uninterrupted run could be higher, since the process was killed.
- Headroom, now against before: 2,048 MB / 260 MB was about 7.9 times spare; now 2,048 MB / 3,174 MB = 0.65, so the job needs 1.55 times the box (arithmetic from the user's numbers).
- Memory per edge, a consistency check: 3,174 MB x 1,024 / 4.6 million edges is about 0.71 KB per edge, against about 0.68 KB per edge before (260 MB x 1,024 / 390,000). Memory has scaled with the edge count, so the growth is real and not a one-off spike.
- Stated by the user: the job must run on review-01, certified as it is with 2 GB of RAM; a bigger box is off the table because changing it means re-certification. A 4 GB box, as Felix suggests, is therefore not an option this decision may use.
- Stated by the user: the CISO's rule is that as long as the job fits on review-01 it stays as it is, and if it ever does not fit in those 2 GB, it moves to the graph database on the certified security cluster, with no tuning tricks to squeeze it back in. The condition in the rule is now met.
- Stated by the user: Hannes keeps pushing for the graph database security licensed last year.
- Load and freshness (unchanged, user's number): a batch job run once a night at 02:15 by cron on review-01 (crontab.txt); the identity provider drops the export every evening (README.md), so answers are up to a day old. The 4-minute run time was measured at the old size; it has not been measured at the new size.
- Process: one process runs the job and holds one copy of the graph (review/reach.py: `main` loads once, then runs 4 walks).
- unknown: the nightly time window and the run time at the new size; no log of the failed runs is in the repo. Looked in the repo files only.
- unknown: how much of the 2 GB the operating system and other services on review-01 use, the grant edge count and the nesting depth; exports are not in the repo (export/ is gitignored). Nothing was measured here.
- unknown: expected growth after the consolidation; no history is in the repo.

## Options considered

- graph-database (the graph database security licensed last year, on the certified security cluster): chosen, because the job peaked at 3.1 GB (was 260 MB) against the 2 GB limit of review-01 on 4.6 million edges (was 390,000), and the CISO's rule names this database as the destination when the job no longer fits. The trial to pass before money is committed: load the full 410,000 identities, 52,000 groups, 4.6 million membership edges and the grants, and run the 4 reachability queries of review/reach.py to completion.
- in-process-library (networkx on review-01): rejected, because it has been measured failing: two nights of OOM kills at 3.1 GB against 2 GB, 1.55 times the limit. The remedies that remain (a bigger box, or squeezing the graph smaller) are closed: a 4 GB box needs re-certification, and the CISO's rule forbids tuning tricks. A 4 GB box would also leave only 4,096 / 3,174 = 1.3 times headroom at today's size, with the edge count already 11.8 times larger than at the last decision.
- recursive-sql (recursive queries on a SQL database): rejected, because there is no SQL database in this repo to run them on, the data arrives as JSON-lines files, and the rule sends a job that no longer fits to the graph database, not to a new store of another kind.
- no-graph (plain joins, no traversal): rejected, because the review follows nested groups to a depth that depends on the data.

## What would change the decision

- The CISO changing the rule, or the auditors accepting re-certification of a larger review-01 (a decision for the CISO and the auditors), would reopen the in-process-library option. Cost of a 4 GB box against 3.1 GB measured peak: 1.3 times headroom, so it would need a measured peak after the next export to confirm it.
- The trial on the security cluster failing: the 4 queries not finishing inside the nightly window at the full edge set (the security owner sets the window), or the cluster not being able to take the nightly load of the export, would send this back for a new look.
- The export shrinking back, for example the subsidiaries' directories leaving the SSO, to a peak under 2 GB on review-01 with room to spare would, under the CISO's rule, put the job back on networkx; watch peak memory each night.
- A requirement for answers fresher than the nightly export would change what the graph database is fed with; the security owner sets that limit.
