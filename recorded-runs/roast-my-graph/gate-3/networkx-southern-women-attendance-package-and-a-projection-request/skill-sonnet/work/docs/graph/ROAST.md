# Roast: events/ (model.py, analysis.py)

Verdict: Nothing serious, and the list is empty. The TA is not right: the event nodes are not a join table in disguise, and projecting to women-to-women and dropping them would break three of the four class questions. Change nothing before class.

Judged against:
- Engine and version: NetworkX, version not stated (README.md). Davis Southern Women data: 18 women, 14 events, 89 attendances (README.md). Confirmed by running the loader.
- Workload: a class package that prints an answer key from `events/analysis.py`; batch, tiny, nothing interactive (README.md).
- Writers: none. The graph comes from `nx.davis_southern_women_graph()` and is never modified.
- The four questions the package must answer (README.md): event sizes, the two groups of women, events bridging the groups, events two given women both attended.

## Findings

None.

The schema is accused of being a join table, which is a bold charge against two sets of nodes that are literally the data. Somewhere a projection is being sharpened to throw away the 14 things the women did together.

## Holds up
- `attendance`: the event nodes are a second kind of node with their own questions asked of them, not a node sitting between two others with only its two sides touching it. Questions 1, 3 and 4 are about events: `event_sizes` reads event degree, `bridging_events` returns events, `shared_events` returns events. A woman-to-woman projection stores only a count per pair of women. It cannot say which events two women shared (question 4: Evelyn Jefferson and Nora Fayette shared E6 and E9), cannot say how big an event was (question 1: E8 had 14 women), and cannot say which events bridge the two groups (question 3: E6, E7, E8, E9). Dropping the events would remove the data these three answers come from. It would only be right if every question were about pairs of women alone, and three of the four are not. The graph is also not edge-with-properties in disguise: an attendance edge has no properties, and the events are things women attend, which others are counted against.
- `co_attendance`: the projection is already built, once per call, from the bipartite graph, for the one question that needs it (question 2). Keeping both the bipartite graph and the projection derived on demand is the right shape here, and no stored copy can fall out of step with it. At 18 by 14 the rebuild costs nothing.
- `groups`: modularity communities on the weighted projection, run on the shipped data, give exactly two groups (10 and 8 women), so taking the first two matches the class question.
- `event_sizes`, `shared_events`, `bridging_events`: each reads the edges in the direction the graph stores them. Checked by running `events.analysis`, and the printed answers are consistent with the data.

## Not checked
- The NetworkX version is not stated in the repo. `greedy_modularity_communities` is deterministic for this input in the installed version; behaviour in other versions was not checked.
- No files were edited.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
