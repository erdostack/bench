Short answer: the reviewer is wrong, and I would not make that change.

The event nodes are not a join table in disguise. In the Southern Women data the 14 events are entities with their own properties: how many women came and which ones. A woman-to-woman edge with a list of events is the one-mode projection with a list attached, and it loses structure. An event with 5 attendees becomes 10 pairwise edges that look the same as 10 separate two-person meetings, and the bundle of "these five were all at the same event" is gone. Your README says students use this module to compare the two-mode graph with its one-mode projections. If you store only the projection, the module has nothing left to compare against. The claim that the co-attendance numbers "come straight off the edges" is already true of `co_attendance`, which uses `weighted_projected_graph`. If you want the shared-events list on a pair, `events_shared` already gives it.

Problems in the code itself:
- `events_shared` sorts with `int(e[1:])`, which assumes every shared node is named `E<number>`. I called it with two events to see the women they share, and it raised `ValueError` ('velyn Jefferson'). A name not in the graph raises a bare `KeyError`. The function doesn't check that its arguments are women.
- `who_was_at` accepts any node. I called it with a woman and got her events back.
- The tests don't touch `events_shared` and only check the maximum of `event_sizes`, so they would not have caught the first problem.
- `load` returns women and events as a bare tuple, and the order is documented only in a comment.

All six findings, including the review comment (rated high), are in `findings.json` in the repo root. I changed no code.
