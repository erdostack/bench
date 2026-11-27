Position: keep

Jonas, the outage is the reason we looked at this properly, and the cause matters. The old blockers query had no
guard against loops. People mark tickets as blocking each other, and there are about 1,700 such loops in the data;
the query went round one of them until the 30 s statement timeout, and about 40 of those piled up at once. That
would happen in any database that walks without remembering where it has been.

Lukas fixed it in October: the query carries the path and skips tickets already on it. Since then the panel's query
runs at 11 ms p95, against a 300 ms budget, at about 40 loads a second, on 2.4M tickets and 900k blocking links.

So we decided to keep the recursive query on Postgres. Moving to Neo4j would mean a second copy of the ticket links
kept in sync, to solve a problem that is already solved. If the guarded query ever gets near 300 ms, we reopen it.
