Decision: in-process-library. Written up in docs/graph/DECISION.md.

This is an assignment problem: 58 judges, 164 projects, once a year. As a max flow with each judge's capacity
at this year's limit of 3, networkx judged all but 2 projects in about 40 ms, where the current first-come loop
leaves 11 without a judge. Note that MAX_PER_JUDGE in fair/assign.py is still last year's 5. A graph database
would be a server for a script that runs once a year.
