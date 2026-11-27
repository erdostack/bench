# Judge assignment

Decision: graph-database

## Workload facts (from the conversation, 2026-11-23)

- 58 judges, 164 projects. Runs once, the week before the fair, on a laptop.
- This year's committee rule: a judge takes AT MOST 3 projects. MAX_PER_JUDGE = 5 in fair/assign.py is last
  year's value and is wrong now.
- Eligibility (already in the code): the judge covers the project's category and is not from its school.
- First-come loop with the cap at 3: 11 projects unjudged. networkx max flow: all but 2. About 40 ms.

## Options considered

- graph-database (a committee parent's Neo4j): rejected; a server for a once-a-year script.
- in-process-library: chosen; max flow in networkx.
- recursive-sql: rejected; this is an optimisation, not a traversal.
- no-graph: rejected; the greedy loop is exactly what fails.

## What would change the decision

- Nothing at this size. Preferences or panels of two judges would change the model, not the tool.
