Decision: recursive-sql

A friends list is a walk over the friendship graph, and SQLite can walk it: a WITH RECURSIVE query over person_knows_person with a depth limit gives the friends, joined to person to drop closed accounts. 160,000 friendships at 20 opens a second is fine for that. No Neo4j. Recorded in docs/graph/DECISION.md.
