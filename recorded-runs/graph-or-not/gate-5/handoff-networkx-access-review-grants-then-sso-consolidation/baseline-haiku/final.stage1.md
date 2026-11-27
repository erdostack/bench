Decision: in-process-library

Keep the access review where it is: load the export into memory and run it with networkx on review-01, as the job does today. The decision follows the CISO's rule. That rule moves the job to the graph database only if it stops fitting in the 2 GB on review-01, and it does not fit a trigger today.

Why:
- Reach through nested groups and grants is a traversal (reverse reachability from each system node), so the problem is a graph problem and "no-graph" is wrong. But the problem is also small enough for the box. The networkx graph peaks at about 260 MB against 2 GB of RAM, about 13% of the limit, and the job finishes in 4 minutes once a night.
- The rule's trigger is not met, so the graph database and its security-cluster move are not needed now. Licensing a graph database for this job would add cost, and the move would require the data to leave review-01.
- Recursive SQL could do this too, but the rule says the job stays as it is while it fits, and a change of engine is a change to the certified setup. Nothing here justifies re-certifying review-01.

Suggested follow-up (not a tuning change):
- Record the peak memory of each nightly run in the log, for example by logging resource.getrusage(resource.RUSAGE_SELF).ru_maxrss after load. That lets the team see the trend against the 2 GB limit and act on the CISO's rule when it is actually reached, instead of estimating it.
- Keep the 260 MB figure as a measured number from the current export. Growth in identities, groups or memberships moves it, and the record would show when it approaches the limit.

Caveat: the 260 MB peak and 4-minute runtime are the figures given in the request. They were not reproduced here, because the export is not in the workspace, and the RSS of the whole Python process (beyond the graph) was not measured.
