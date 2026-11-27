Decision: in-process-library. Written up in docs/adr/0007-quest-reachability-and-prerequisite.md.

Both checks are whole-graph questions over content that lives in the PR itself: reachability from the start quests
and cycle detection in `requires`. At 22k quests and 61k edges networkx does both in memory, and your prototype already
runs in 1.8 s including YAML parsing, about 40 times a day. A graph database would need loading from the PR's YAML
before every check, and someone to run it; you have no ops team and nobody on call. Recursive SQL has no database to
run on here.
