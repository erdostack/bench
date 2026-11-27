Still stands: yes

Recursive SQL on the existing query stays the decision. The numbers, old against new:

- Researchers: 41,000 against 390,000 (9.5 times)
- Advising rows: 46,500 against 452,000 (9.7 times)
- Deepest lineage: 19 against 27 generations (the query stops at 30)
- Tree page p95: 18 ms against 64 ms (3.6 times, for 9.5 times the researchers)
- Trigger for a graph database review: p95 above 120 ms. Headroom went from 6.7 times to 1.9 times.
- Budget: 250 ms. Share used went from 7% to 26%.

The 64 ms p95 is below the 120 ms trigger, so the condition for changing the decision is not met. The decision record was updated with the new numbers beside the old ones. The Decision line did not change.

Not checked here: the database and the staging copy are not in the repo, so the 64 ms figure is your measurement, not mine. Two things to confirm:

1. Whether staging runs on production hardware. If it does not, the 18 ms and 64 ms figures are not directly comparable. The trigger is a production p95, so a production run with the full register is the real test.
2. The query stops at 30 generations. The register is at 27 now. A lineage deeper than 30 would be cut short without an error. Someone should decide whether the cap is right before the next import.

The route count per walk is still unmeasured. The query returns one row per route, so this is the open risk for the rewrite option. Counting it on a staging copy is a cheap check.

Nothing outside docs/graph/DECISION.md was changed.
