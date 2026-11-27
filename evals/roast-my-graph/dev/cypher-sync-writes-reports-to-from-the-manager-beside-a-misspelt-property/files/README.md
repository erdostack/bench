# orgline

The company's reporting lines as a graph, fed from the HR system and read by the expenses tool and the
intranet. Neo4j 5.

| Path | What |
|---|---|
| `docs/model.md` | the model in one table |
| `graph/schema.cypher` | constraints and indexes |
| `graph/sync.cypher` | what the nightly HR sync runs (rows arrive as `$rows`, 2,000 at a time) |
| `graph/queries.cypher` | the read queries, each with a `// name:` line |

Numbers: 48,000 employees, 3,100 teams, 60 sites. Nobody is more than nine levels below the chief executive.

HR sends the complete list every night. The sync upserts the employees, then, in one transaction, removes
the three kinds of relationship (`clear_lines`) and writes them again from the export.

Who calls what:

- `approver_for`: the expenses tool, for every claim submitted (about 6,000 a day). The claim is routed to
  whoever this query returns.
- `chain_of_command`, `direct_reports`, `team_roster`: intranet profile and team pages.
- `headcount_under`: the quarterly planning export.
