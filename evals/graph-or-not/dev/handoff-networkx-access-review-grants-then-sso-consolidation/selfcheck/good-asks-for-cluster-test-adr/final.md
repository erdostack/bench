Still stands: no.

ADR 0006 tied the in-process call to review-01's 2 GB; the job now peaks at 3.1 GB (it was 260 MB). By the CISO's
rule it moves to the graph database on the security cluster, and a bigger box is out because review-01 is the
certified one. Before switching the cron over I'd do one test run on the cluster to get the review's time on 4.6M
edges, so I marked it need-more-information until then.
