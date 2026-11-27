Your TA is wrong, so keep the event nodes.

The projection to a woman-to-woman graph does keep the co-attendance counts. That covers question 2 (the two groups) and nothing else. Once the events are gone you can no longer answer:

1. Which events were the big gatherings. The projection has no events, so event sizes are lost. The answer key gives E8 (14), E9 (12), E7 (10), E5 (8), E6 (8).
3. Which events brought both groups together. This needs the event nodes. The answer key gives E6, E7, E8, E9.
4. Which events Evelyn Jefferson and Nora Fayette both attended. This needs the event nodes. The answer key gives E6 and E9. The projection only gives the count of shared events, not which ones.

I ran the code. The two groups from greedy modularity on the projection are 10 and 8 women, and the projection is connected (18 nodes, 139 edges). Those results depend on the events, so the events have to stay.

Changes before class:
- Keep `events/model.py` as it is. The bipartite graph is the right model, and the projection is a helper for question 2 only.
- In `events/analysis.py`, check that `groups` returns exactly two communities before unpacking `[:2]`, so a silent change in the data or the networkx version fails loudly.
- Check that "Evelyn Jefferson" and "Nora Fayette" exist before calling `shared_events`.
- Add a small test suite for the helpers, pinning the numbers above, so the answer key cannot quietly drift.

The findings are in findings.json. One more point, not a code defect: the answer key sits in the same package as the exercise helpers. If students get the repo, they get the answers, so consider keeping `analysis.py` out of the student copy.
