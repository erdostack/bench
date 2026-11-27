Decision: in-process-library

Build the linked-accounts panel as a connected-component lookup over device ids and payment cards only, with networkx, which is already installed. Load those signal rows once per process from the nightly copy and cache the graph. At 1.1M signal rows this fits easily, so the walk should stay well inside 2 s, though that is not measured yet. A graph database (Bilal's proposal) costs more than 200 lookups a day justify.

Three things need fixing, and they matter more than the choice of tool:

- The current code links accounts through shared IPs. The join in `moderation/links.py` has no kind filter, so `ip` signals count. Trust and Safety's rule says they never link, so the walk must use only `device` and `card` rows. The panel is wrong in both directions: it adds IP links the rule forbids and misses chains deeper than three steps.
- The 31 of 400 groups were found against networkx `connected_components` on last week's copy. If that reference included IP edges, it measured the wrong rule. Recompute it on device and card only before reporting the figure.
- Nothing was run on a real copy, and no load time or lookup time was measured. The repo has no copy of `var/forum.db`.

Open questions for Ayla and the moderators:

1. How many of the 1.1M signal rows are device or card rows?
2. Is "linked" transitive, so that A and C count as linked when A shares a card with B and B shares a device with C? The reference comparison assumes it is.
3. Are nightly copies acceptable, or do moderators need the panel on live data? If live, recursive SQL on the live database is the better fit.

If a recursive query with a device and card filter, run on the nightly copy, returns every lookup under 2 s, recursive SQL becomes the simpler choice, because it needs no load step. Only the decision file docs/graph/DECISION.md was added to the repo; `moderation/` is unchanged.
