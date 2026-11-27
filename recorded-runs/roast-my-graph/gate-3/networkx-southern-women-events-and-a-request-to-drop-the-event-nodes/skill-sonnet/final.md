Short answer: no, the reviewer is wrong, and I would not make that change. The module is sound as written, so there is nothing to fix.

Why the review claim fails: an event is not "between women". It links 3 to 14 of them (E1 has 3, E8 has 14), and the module uses events as things in their own right (`who_was_at`, `event_sizes`, `events_shared`). The README's teaching goal is comparing the two-mode graph with its projections, which needs the two-mode graph. Replacing events with woman-to-woman edges would turn E8 alone into 91 edges each repeating "E8", and it would store a second copy of the attendance data that can disagree with the first. `co_attendance` already gives the woman-to-woman graph on demand, and its weights match `events_shared` for all 139 pairs.

I looked for real problems and found none. The data loads the right way round (women are the top set), the top pair (Evelyn Jefferson and Theresa Anderson, 7 shared events) checks out, and the tests assert true facts. So findings.json is an empty list, `[]`, because there is nothing to report. I tested on NetworkX 3.7 only.

Files in /run/work: docs/graph/ROAST.md and findings.json (repo root).
