# Related sessions

Decision: no-graph

## Workload facts (given by the owner, 2026-11-23)

- Related = sessions sharing at least two tags (programme committee). Nothing further.
- About 1,400 sessions, 9,000 session-tag rows, one SQLite file rebuilt every evening; about 3,000 attendees.

## Options considered

- graph-database (Tove's suggestion): rejected; a server to run for one self-join.
- in-process-library, recursive-sql: not needed; nothing is walked.
- no-graph: chosen. Self-join on session_tag, HAVING count >= 2.

## What would change the decision

- The committee asking for something that follows links further (related to related).
