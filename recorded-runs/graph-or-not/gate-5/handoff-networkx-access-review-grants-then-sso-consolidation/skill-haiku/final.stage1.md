Decision: in-process-library

Keep the review where it is: the networkx graph that runs nightly on review-01 peaks at about 260 MB (stated) against 2 GB of RAM, about 13 percent of the box, and the job takes about 4 minutes. A synthetic graph of the stated size measured 190 MB traced, the same order, so the figure looks right. Under the CISO's rule the job stays as it is, and no graph database is needed now.

What would move it: the real peak under load reaching the 2 GB limit, which would send the job to the security cluster as the rule says. The real export, the nesting depth, the grant-edge count, the growth rate and any other processes sharing review-01 were not in the repo or stated, so the headroom is an estimate. Nothing in the repo was changed except the new file docs/graph/DECISION.md.
