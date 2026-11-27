# Referral bonus recipients

Decision: no-graph

Rule (docs/rules/referral-bonus.md): level 1 = referrer, level 2 = referrer's referrer, nobody further.
Workload (2026-11-23): about 1.3M members; longest chain 26; about 4,000 first paid months on a busy day; nightly job.

Rejected: graph database and graph library (two indexed lookups per new member); recursive SQL (fixed depth of 2).
