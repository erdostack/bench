# Trapped-junctions check for the one-way consultation

Decision: in-process-library

## Workload facts (from the conversation, 2026-11-24)

- Traffic team's rule: a junction is TRAPPED if, under the draft's directions, you cannot drive from it to the
  ring road OR cannot drive to it from the ring road. Both directions are required.
- Footpaths (segment.mode = 'foot') are not roads. A junction only on footpaths is not reported.
- Current oneway/trapped.py only looks outward and gives up after 25 steps (MAX_STEPS): on last week's draft it
  flagged 63 junctions, most of them on the long one-way market-streets loop, which is fine.
- A draft is about 1,450 junctions and 1,900 segments; two planners run 20 or 30 drafts a week on laptops.

## Options considered

- graph-database (consultant): rejected; a server for a file exported many times a week.
- in-process-library: chosen. networkx DiGraph of the road segments; reachable from the ring and reaching it.
- recursive-sql: would work on files this size (two recursive queries from the ring), but the check is Python.
- no-graph: no; reachability is the question.

## What would change the decision

- Checking every draft for the whole city at once, interactively in the sketch tool.
