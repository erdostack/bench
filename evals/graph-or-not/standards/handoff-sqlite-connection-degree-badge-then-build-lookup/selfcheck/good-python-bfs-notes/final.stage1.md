Decision: in-process-library

Small enough to walk in the app: 610,000 friendships is a few tens of MB as adjacency lists, and a breadth-first
search that stops after 3 steps from each viewer touches a few thousand members, well within the 50 ms the badge
gets at 30 views a second. Neo4j is a second store for a bounded walk. The PM's rule (beyond 3 steps or no path is
-1, own profile 0) is in notes/badge.md.
