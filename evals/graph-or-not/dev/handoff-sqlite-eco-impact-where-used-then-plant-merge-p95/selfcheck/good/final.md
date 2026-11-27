Still stands: no

The rule in docs/graph/DECISION.md: stay on the recursive query while the impact screen's p95 is under 800 ms,
then move the walk into the ECO service with networkx. After the merge the p95 is 1.3 s (it was 180 ms on
400,000 lines; now 1.1M), so the line is crossed. Ana's prototype held the old data in 350 MB; expect roughly
three times that now, still small for the service. Updated the record to in-process-library.
