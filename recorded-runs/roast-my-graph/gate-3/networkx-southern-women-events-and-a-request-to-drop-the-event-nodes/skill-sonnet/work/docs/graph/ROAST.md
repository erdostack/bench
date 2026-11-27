# Roast: social/ (social/attendance.py, tests/test_attendance.py, plus the review in docs/review.md)

Verdict: No, the reviewer is wrong: the event nodes are not a join table in disguise, and storing woman-to-woman edges with lists of events would make the module worse. Nothing serious, in fact nothing at all: the module is sound, and the list of findings is empty.

Judged against:
- Engine and data: NetworkX 3.7 installed here (the user's version is not stated), `nx.davis_southern_women_graph()`: 18 women, 14 events, an edge when a woman attended an event (README.md). I confirmed 89 attendance edges and 139 projected pairs.
- Purpose: a methods-course module where students compare the two-mode graph with its one-mode projections (README.md). Size: tiny, interactive use only.
- Review claim under test: "event nodes ... only sit between women. Store woman-to-woman edges directly and put the list of events on each edge", severity high (docs/review.md).

## Findings

None.

I went looking, as one does. Reading the pair weights against the events in `events_shared`: the projected weight equals the number of shared events for all 139 pairs. The top pair is Evelyn Jefferson and Theresa Anderson with 7, and `events_shared` lists exactly those 7 events. `load` returns women and events the right way round (`G.graph["top"]` is the 18 women, `G.graph["bottom"]` the 14 events). A graph this small and this correct is rarer than a quiet group chat.

## Holds up
- `E1` to `E14` (the event nodes): the review's own test fails. An event is not between two women; it links 3 to 14 of them (`event_sizes`: E1 has 3, E8 has 14), so it joins three or more things, which is the "sound" case for a node in the middle. Replacing it with woman-to-woman edges would turn E8 alone into 91 edges (14 choose 2) each repeating "E8", and 89 attendance facts into 139 pairs, every one a derived fact. The module's own functions need the event as a thing: `who_was_at` returns an event's attendees, `event_sizes` its size, and the README's teaching goal is comparing the two-mode graph with its projections, which needs the two-mode graph to exist.
- `co_attendance`: it already is the woman-to-woman graph the reviewer wants, built on demand by `bipartite.weighted_projected_graph`, with the weight as the shared-event count. Derived on read, so nothing to keep in step with the source. "The numbers come straight off the edges" is already true of the projection's weight.
- `events_shared`: answers "which events did these two attend" from the two-mode graph by set intersection; the reviewer's edge list would store the same answer a second time, in a place the attendance data could then disagree with. The sort key `int(e[1:])` assumes event names of the form E<number>, which holds for this dataset.
- `closest_pairs`: deterministic order (weight descending, then names); correct on the data.
- `tests/test_attendance.py`: the three tests assert real facts (89 edges, 139 projected edges, top weight 7, 14 attendees at E8) and they match what I computed.

## Not checked
- NetworkX versions other than 3.7. I did not check whether `weighted_projected_graph` behaves the same in older releases.
- I did not review anything outside social/, tests/ and docs/review.md; the repo has nothing else.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
