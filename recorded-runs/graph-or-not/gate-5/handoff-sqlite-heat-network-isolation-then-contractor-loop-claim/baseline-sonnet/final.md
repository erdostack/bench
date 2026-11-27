Position: keep

Reply to send (I found no written record of the original decision in the repo, so the "what we decided" line is inferred from the code and README; correct it if the decision was worded differently):

> Thanks for looking at it. We are keeping the recursive SQL query for the isolation screen. It does not loop on the ring mains, so the reason to switch does not apply.
>
> - What we decided: the isolation screen stays a recursive query (`sql/isolate.sql`) over the SQLite network model (`var/heatnet.db`), with no graph database.
> - Why it terminates on rings: the walk is `WITH RECURSIVE fed(node_id) ... UNION` (not `UNION ALL`) and keeps only the node id. SQLite drops any row already in the result, so a node reached a second time is not expanded again. A ring is walked once around and stops. Recursion only runs forever when each row carries something that makes it unique (a hop counter or a path) and nothing bounds it. This query has neither.
> - Checks I ran: a 3-node ring main with two substations. Isolating a ring pipe returns no buildings, since the heat reaches around the other way. Isolating a spur pipe returns only the building on it. A self-loop pipe also terminates. All three finish instantly.
> - Timing on synthetic rings: one ring of 2,000 junctions plus 500 extra cross-links, with 2,000 substations, took 0.04 s. At 20,000 junctions and 5,000 cross-links it took 0.39 s. These are synthetic networks, not our real `heatnet.db`, but they show cost grows with pipe count, not with the number of loops.
> - On "graph databases handle cycles natively": they do so by tracking visited nodes, which is the same thing `UNION` does here. For one reachability question per pipe on a network this size, we gain nothing and would add a second system to run and load.
>
> If you have a specific ring main where it hangs, send the pipe id and we will look at that data. As written, the query should not.
