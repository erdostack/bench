# Roast: clubgraph/ (people you may know)

Verdict: Not nothing, and two of the three problems are in `suggest`. The walk goes through interest hubs, so a call costs time in proportion to how many users share an interest, which the README puts at about 1.3 million for `music`. The score also counts shared interests as if they were mutual friends, and ties are broken by load order, which is why the list looks random. The fix is one filter in `suggest`: walk friend edges only.

Judged against:
- Friend suggestions for the home page "people you may know" box, with a 100 ms budget per call: `README.md`, and `clubgraph/build.py` (`load`) for the graph shape.
- Production (November 2026): 2.1 million users, 9 million friendships, 15 interests. `music` on about 1.3 million users, `cooking` on about 700,000, the smallest on a few thousand: `README.md`.
- Sample data is 3,000 users, 16,410 friend edges and 5,226 interest edges, generated with the same shape: `README.md`, `data/`.
- Graph: one `nx.Graph`. Users are nodes with `kind="user"`; interests are nodes named `interest:<name>` with `kind="interest"`; edges carry `kind="friend"` or `kind="likes"`: `clubgraph/build.py`.

## Findings

### high: `suggest`
Problem: `suggest` walks every neighbour of the user, including interest nodes. For `music` it then walks every user who likes it. README: `music` is liked by about 1.3 million users, so one call iterates that many nodes before it returns. Measured on this machine with a synthetic hub of the same shape: 65 ms for 100,000 fans and 275 ms for 300,000, so about 0.9 µs per fan. Extrapolated (not measured at prod size), `music` alone is about 1.2 s per call, against a 100 ms budget stated in the README.
Fix: Walk friend edges only. Change the inner loops to skip any neighbour whose edge `kind` is not `"friend"`, at both levels. Measured on the same 300,000-fan hub: 0.06 ms for the friend-only walk. If the product still wants shared-interest suggestions, precompute them offline per user rather than walking the hub at request time.

### medium: `suggest`
Problem: The score counts a shared interest the same as a mutual friend (both are paths of length two through a neighbour). The docstring says "ranked by how many neighbours they share", and the README says "friend suggestions", so the files disagree on what the box is for. Sample: 32 of 2,000 suggestions (1.6%) have no mutual friend at all, and for many users the top ten order changes once interest matches are removed. At prod scale, a stranger who shares two common interests scores as high as someone with two mutual friends.
Fix: Decide what the box is for. If it is friend suggestions, score mutual friends only (the friend-only walk above). If shared interests should count, keep them out of the same score: rank by mutual friends first and use shared interests only as a tie-break, and say so in the docstring.

### medium: `suggest`
Problem: `Counter.most_common(k)` breaks ties by first-seen order. Most candidates score 1, so the top ten are whoever happened to appear first in the adjacency walk, which follows the order of rows in `data/friendships.csv`. Synthetic check: with 300,000 candidates tied at score 1, the top three were `x0`, `x1`, `x2`, the first three loaded. This is the mechanism behind "the suggestions are random".
Fix: Sort candidates by `(-score, m)` (or by a real secondary signal such as shared interests) before taking the top k, so the order is deterministic and explained.

### low: `small`
Problem: `tests/test_suggest.py` builds a four-user path graph with no interest nodes, so the tests only check friend-of-friend ordering. Neither the interest walk nor the tie-break is exercised, which is why the ranking and speed problems are not caught.
Fix: Add a test with one friend-of-friend and one stranger who shares two interests, asserting the friend-of-friend is returned first, and a test with an interest hub of a few thousand users asserting the call finishes within a set time.

## Holds up
- `mutual_friends`: reads only friend edges (`G.edges[a, n]["kind"] == "friend"`) and returns a sorted list. It is correct for the box's mutual-friend text, and it is the friend-only logic `suggest` should follow.
- `known` set in `suggest`: excludes the user and their friends before scoring, so existing friends are never suggested. Holds for any graph shape.
- Interest nodes are named `interest:<name>` and tagged `kind="interest"`, and the candidate check `G.nodes[m]["kind"] == "user"` keeps interest nodes out of the results. A user id can never collide with an interest name. Holds as written; the problem is the walk, not the output filter.
- `load`: one node per user and one edge per friendship or like; a duplicate friendship pair collapses into one edge, so the friend degree is not inflated by the CSV listing a pair twice.

## Not checked
- Production: no prod graph, query logs or latency was available. All prod-scale numbers are from the README, and the timing at prod size is an extrapolation from synthetic graphs on this machine.
- Friend-degree distribution at prod scale is not stated, so the cost of friend-of-friend walks for very well-connected users is unknown.
- The friend-only fix was checked in memory against the sample (it changes the top ten for most sampled users; it was not compared with a product spec, because none exists in the files).
- Ran `pytest` (2 passed) and the synthetic hub timings. No other engine was in scope.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
