# Roast: social (Southern Women two-mode teaching module)

Verdict: Nothing serious in the code, and the review is wrong. The event nodes are not a join table in disguise. Each one joins between 3 and 14 women, and a single edge joins exactly two nodes, so an event with several attendees cannot be stored as one woman-to-woman edge. The proposed design would turn 89 edges into 139 and repeat event ids 322 times. Keep the event nodes.

Judged against:
- README.md: 18 women, 14 social events, an edge when a woman attended an event; the module is for comparing the two-mode graph with its one-mode projections.
- Measured on `nx.davis_southern_women_graph()` (NetworkX 3.7): bipartite, undirected, simple; 32 nodes and 89 edges. Event sizes run from 3 (E1, E2, E13, E14) to 14 (E8). Women attend 2 to 8 events each.
- docs/review.md: suggests woman-to-woman edges with `G[a][b]["events"]`, and rates the point "high".
- Measured against that proposal: 18 nodes and 139 edges (every pair that shares an event), with 322 event-list entries in total. The sum of C(k, 2) over the events is also 322. The co-attendance weights that `co_attendance` already produces equal the length of each proposed event list, so that benefit is already there.

## Findings

### low: `events_shared`
The function sorts event names with `int(e[1:])`, which assumes every event is named `E` followed by a number. The shipped names all fit that pattern. A differently named event (for example a student adds "Picnic") would raise a `ValueError` here.
Problem: When `events_shared` runs on a graph whose event names do not start with `E` followed by digits, the sort key fails. The README does not state that event names follow this pattern, so this is a question to confirm, not a defect in the shipped data.
Fix: sort by the node's position in the `events` list passed in, or sort plainly by name, if the module ever takes a different event naming scheme.

### low: `closest_pairs`
The tie-break sorts on `e[0]` and `e[1]`, which are the endpoint order that the projection happened to store, not an alphabetical order. The output lists some pairs with the later name first, for example `('Laura Mandeville', 'Brenda Rogers', 6)`.
Problem: When two pairs have the same weight, the displayed order of names within each pair depends on how the projection stored the edge, not on name. The ranking is deterministic for this graph, so nothing is wrong numerically; it only looks inconsistent to students.
Fix: normalise each pair (for example `tuple(sorted((u, v)))`) before the sort, so names always appear in alphabetical order.

## Holds up
- Event nodes (`who_was_at`, `event_sizes`, `events_shared`, `co_attendance`): each event joins 3 to 14 women. A relationship can join only two nodes, so an event with three or more attendees is a shape that needs its own node, which is the third thing the review calls a join table. Replacing it would lose the event as an object (its size and its attendee set) and would need 322 event-list entries to say what 14 nodes already say.
- `co_attendance` with `bipartite.weighted_projected_graph`: the weight on each woman-to-woman edge equals the number of shared events, and the projection has 139 edges with no isolated women.
- `event_sizes` with `G.degree(e)`: correct, because the graph is bipartite and an event's neighbours are the women who attended it.
- `who_was_at`: returns the women attached to an event, sorted. It is correct for this bipartite graph.
- `load`: `G.graph["top"]` is the list of women and `G.graph["bottom"]` the events, as the comment says, and the test checks the counts.
- The tests assert 18 women, 14 events, 89 edges, 139 projected edges, a top pair weight of 7, and E8 with 14 attendees. All of these match the measurement.

## Not checked
- docs/review.md is the only source for the reviewer's claim. I did not check it against the course materials, if any exist.
- `python -m pytest tests` was run: 3 passed. The counts above were also measured directly from the same NetworkX calls the tests use.
- `events_shared` and the tie-break in `closest_pairs` have no tests, so no test would catch a change in either.
- The proposal's 139-edge count assumes every shared pair gets one edge. I did not build or test a version of the proposed design beyond counting it.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
