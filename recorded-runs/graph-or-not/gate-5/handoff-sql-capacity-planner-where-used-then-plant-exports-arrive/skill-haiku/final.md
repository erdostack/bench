Decision: in-process-library

The three plants total 1.2 million BOM lines, and the networkx load on your test host held them at 1.4 GB resident, inside the 2 GB allowance, with where-used for all 40,000 components done in 3 minutes, inside the 10-minute window. That is the figure the earlier call was waiting for, so I have moved the decision from need-more-information to in-process-library. The current recursive SQL call is not the answer: at 90 ms per call it works out to about 60 minutes for the 40,000 components, six times the window.

Two things must hold before go-live, and neither is measured yet:
- The load time. The 3 minutes covers only the where-used run, so loading the BOM has to fit in the roughly 7 minutes left in the window. If it does not, the fallback is a set-based recursive query on Postgres, which has not been run.
- One copy of the graph per host. Two copies at once would be about 2.8 GB, over the allowance.

The 1.4 GB and 3 minutes come from a test host, not the planner host, so measure the planner host too.

Updated: `docs/graph/DECISION.md`, with the new BOM figures added and the earlier "unknown" BOM size marked as replaced. Nothing else in the repo was changed.
