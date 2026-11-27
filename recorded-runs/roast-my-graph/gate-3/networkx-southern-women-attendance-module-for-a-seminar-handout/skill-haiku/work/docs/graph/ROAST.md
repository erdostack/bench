# Roast: seminar/ attendance counts

Verdict: Nothing serious, and the halving is not needed. `total_attendances` returns 89, which is the number of edges in the graph, and each edge is one (woman, event) attendance. The graph is bipartite, so summing degree over the women side visits every edge exactly once; halving would give 44.5, which matches nothing in the data. `mean_events` is 89 / 18 = 4.94, also correct.

Judged against:
- 18 women, 14 social events, an edge when a woman attended an event: `README.md`.
- Davis Southern Women graph, sides in `G.graph["top"]` (women) and `G.graph["bottom"]` (events): `README.md`, `seminar/attendance.py` (`load`).
- Output is a one-off printed handout (`python -m seminar.handout > handout.md`): `README.md`.
- Undirected is not a double count here: every edge joins a woman to an event. Checked: the sum of women's degrees is 89 and the graph has 89 edges, and every edge has exactly one woman endpoint.

## Findings

None.

## Holds up
- `total_attendances`: sums degree over the women side only. In a bipartite graph each edge has one woman end, so each attendance is counted once. This would change if women-to-women edges were ever added, since the sum would then count those from both ends.
- `mean_events`: divides by `len(women)`, which is correct for 18 women. An empty list would raise ZeroDivisionError, but the workload is fixed at 18 women, so this is not a defect at this size.
- `co_attendance`: weighted projection onto women, where the weight is the number of shared events. The handout label "events" matches the weight.
- `seminar/handout.py` (`render`): every label matches the number beside it; the busiest-events and companion lists sort and print as written.
- `tests/test_attendance.py`: on a three-edge graph it asserts a total of 3, so a halving or double count in `total_attendances` would fail it.

## Not checked
- Ran `pytest` (1 passed), `python -m seminar.handout` (full output), and checked the graph with NetworkX 3.7 from the work directory: 89 edges, 32 nodes, 18 women, 14 events, bipartite.
- No other engine or sample database was in scope.
- `references/` in the skill was not opened: the NetworkX case did not call for it.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
