# Roast: events/ (attendance graph and answer key)

Verdict: Sound on the questions as written, and the TA is not right. Keep the event nodes. The woman-to-woman projection answers question 2 (the groups) but cannot answer questions 1, 3 or 4, because it keeps only a count of shared events, not which events they were. Nothing serious in the code.

Judged against:
- 18 women, 14 social events, 89 attendances, an edge for each attendance: `README.md`. Event nodes are the second side of a bipartite graph (`bipartite` attribute 0 for women, 1 for events): `events/model.py` (`attendance`).
- Four questions the class answers: event sizes, two groups of women, events that bridge the groups, events two given women both attended: `README.md`.
- Answer key is `events/analysis.py` (`main`), which prints one answer per question.

What the projection keeps, checked by running it: the woman-to-woman graph has 18 nodes and 139 edges, and the Evelyn Jefferson to Nora Fayette edge is `{'weight': 2}`. The answer key gets E6 and E9 for that pair from the event nodes (`shared_events`). Dropping events removes the only place those two event names exist.

## Findings

### low: `main`
Problem: `groups(g, women)[:2]` takes the first two communities and silently drops any others. The shipped data gives two communities (sizes 10 and 8), so the printed answer is right; if a different networkx version or a different partition returned three or more, the key would print two groups without saying so. Confirm whether the class wants exactly two groups before relying on this.
Fix: Assert `len(found) == 2` before unpacking, or print the group count next to the two groups.

## Holds up
- `attendance` and `events` (`events/model.py`): the women set comes from the `bipartite` attribute, and events are the rest of the nodes. Every edge joins a woman to an event (checked: no women-to-women edges among the 89), so the event side is a real second node type, not a join table. Would change only if women-to-women ties were added to the same graph.
- `event_sizes` (`events/model.py`): degree of each event node, which is the number of women who attended it. Matches the answer key output (E8 with 14, then E9 with 12).
- `bridging_events` (`events/model.py`): needs each event's list of attendees to test whether a group member and a non-member both came. The projection cannot answer this; the event nodes are required.
- `shared_events` (`events/model.py`): returns the event names two women both attended. Same reason as above: a count does not give the names.
- `co_attendance` (`events/model.py`): weighted projection onto women, weight = shared events. This is the right structure for question 2 and is used by `groups`. The projection is a derived view, not a replacement for the graph.
- `groups` (`events/model.py`): greedy modularity on the projection, which is deterministic for this graph and returns two communities.

## Not checked
- Ran `python -m events.analysis` (all four answers printed) and checked the community sizes, the 89 women-to-event edges, and the projection weight for one pair, using networkx from the work directory.
- Did not check other networkx versions; the answer key output is only verified for the installed one.
- `references/` in the skill was not opened: this is a NetworkX case and the answers did not need it.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
