Rewrote assign in fair/assign.py as recorded in docs/graph/DECISION.md: a max flow in networkx from projects
to eligible judges, each judge's capacity set to this year's limit of 3 (I changed MAX_PER_JUDGE from last
year's 5). It judges as many projects as the limit allows; projects that can't be placed are left out, and
export.py prints them as UNASSIGNED. networkx needs adding to requirements.txt; I left that file alone.
