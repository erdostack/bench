Position: keep

Marta, we already measured the Postgres route: WITH RECURSIVE with a cycle check ran 7.9 s p95 on a snapshot, the
plan was index scans throughout, and the NOC budget is 2 s. So the decision stands: one impact service holds the
topology in memory with networkx (2.9 GB, 0.4 s per walk) and applies provisioning's ~3,000 changes a day. A closure
table was ~9 billion rows. Happy to walk through the plans.
