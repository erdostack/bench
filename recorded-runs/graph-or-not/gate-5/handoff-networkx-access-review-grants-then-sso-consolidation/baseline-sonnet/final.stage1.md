Decision: in-process-library

Leave the job as it is. Your CISO's rule decides this. It stays on review-01 while it fits in 2 GB, and it moves to the graph database on the security cluster only if it doesn't. The graph peaks at about 260 MB, roughly an eighth of the box, and the whole job runs in 4 minutes on a nightly cron. So it fits and there is nothing to move. I changed no code.

Why not the others:
- Graph database: Hannes's licence is not a reason on its own. It would add a second copy of the identity data to sync and certify, and the reach query is just `nx.ancestors` per sensitive system. The rule gives a clear trigger for moving, and the trigger hasn't been hit.
- Recursive SQL: nothing in the repo is SQL. The data comes from JSON-lines exports, so it would mean building a database for no gain.
- No graph: "who can reach payroll through nested groups" is a reachability query over nested groups. It does need traversal.

Caveats:
- 260 MB is the graph. I'd confirm that the process's peak memory (RSS) for the whole job, including Python and the report writing, is also well under 2 GB. I couldn't measure it here, because there is no export data in the repo.
- Because the rule means "no tuning tricks", the thing to watch is growth. If the numbers grow about 7 times (from 38,000 identities and 390,000 edges), the job no longer fits and it moves to the graph database. A line in the cron log with peak RSS each night would show that coming early and make the switch a planned one.
