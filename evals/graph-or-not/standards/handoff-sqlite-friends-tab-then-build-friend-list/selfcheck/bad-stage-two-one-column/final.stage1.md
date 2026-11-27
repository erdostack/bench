Decision: no-graph

The Friends tab is one lookup: the member's rows in person_knows_person (they can be in either column, since each
friendship is stored once with the smaller id first), joined to person to drop closed accounts. No traversal, so
nothing for Neo4j or a graph library to do.

- 12,000 members, 160,000 friendships, about 20 opens a second: an indexed query, both columns are indexed.
- Legal's rule: friends with a closed account are never listed; suspended accounts still show.
- Bo's Neo4j would be a second store kept in sync for a single-step lookup.

Written up in docs/graph/DECISION.md with legal's rule.
