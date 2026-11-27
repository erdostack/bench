# Roast: seminar/ (attendance.py, handout.py) and its test

Verdict: Nothing serious, and the list is empty. The note's claim does not hold: `total_attendances` does not double count, 89 is correct, and halving it (or `mean_events`) would print a wrong handout.

Judged against:
- Engine and version: NetworkX, version not stated (README.md). `davis_southern_women_graph()` is bipartite and undirected: 18 women, 14 events, an edge per attendance (README.md).
- Sizes: 18 women, 14 events (README.md). Edge count 89, measured by running the loader.
- Operations: one batch script, `python -m seminar.handout > handout.md` (README.md). Nothing interactive.
- Writers: none. The graph is read from the library, not loaded or modified.
- Stated invariant: `total_attendances` is "How many (woman, event) attendances the record has" (seminar/attendance.py docstring).

## Findings

None.

An undirected graph where every edge is counted from both ends, and the whole bit is that the sum runs over one side only. A bipartite graph has no edge with two women on it. The database has been falsely accused and is taking it very well.

## Holds up
- `total_attendances`: it sums degrees over the women side only. In a bipartite graph each attendance edge has exactly one woman endpoint, so the sum is the edge count. Run on the shipped data: sum of women degrees = 89 = `G.number_of_edges()` = sum of event degrees. The graph is bipartite (`nx.is_bipartite` is True). Halving gives 44.5, which is not a count of anything. It would only be wrong if the sum ran over both sides, and it does not. `tests/test_attendance.py` asserts 3 on a three-edge graph, which is the right answer.
- `mean_events`: 89 / 18 = 4.94 events per woman, the right mean for the stated definition. Halving it would give 2.47, which no woman's record supports.
- `co_attendance`: `weighted_projected_graph` gives each woman pair a weight equal to the number of shared events, and each pair appears once in the undirected projection, so there is no double count. Top pair: Evelyn Jefferson and Theresa Anderson, 7 events.
- `events_per_woman`, `attendance_per_event`: plain degree lookups on the correct side of the partition.

## Not checked
- The NetworkX version is not stated in the repo, so no version-specific behaviour was relied on. The checks above are results from the installed library.
- Priya's note proposes a change; no files were edited.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
