# pipeline-graph

CRM graph for the sales org: teams, reps, accounts, deals. Neo4j 5.26 LTS.

- `queries/`: statements used by the sales dashboards and exports; header comment lists parameters and columns.
- `export/`: scripts that turn query results into the CSVs finance and sales ops pick up.
- `docs/leaderboard.md`: what the quarterly leaderboard is for.
