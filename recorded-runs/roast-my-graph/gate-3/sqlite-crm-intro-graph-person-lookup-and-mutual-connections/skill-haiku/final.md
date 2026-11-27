Verdict: the graph part is innocent. The blown budget comes from the email lookup. person_by_email.sql filters on lower(email), and the UNIQUE index on email is case-sensitive, so every sidebar request scans all 1.2 million people. mutual_connections.sql runs as two primary-key searches.

Top findings, worst first:
1. `person_by_email.sql` (high): full scan of person on every sidebar request. Estimated about 144 ms at production size, against an 80 ms p95 budget (linear estimate from the 60,000-row sample). Fix: CREATE INDEX person_email_lower ON person (lower(email)). Verified in memory: same results for 200 sampled emails, and the plan becomes an index search.
2. `email` (low): two spellings of one address could become two people, and the lookup would return an arbitrary one. The sample has none; confirm for production.

Files:
- /run/work/docs/graph/ROAST.md
- /run/work/findings.json

Not checked: no production data, so the 144 ms figure is an estimate; the loader is not in the repo, so its handling of knows direction and email case is unconfirmed.
