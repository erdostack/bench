# Roast: clubgraph/ (build.py, suggest.py)

Verdict: One critical finding explains both complaints. `suggest` hops through the interest nodes as if they were friends, which makes it slow (it visits every user who shares an interest) and makes the ranking look random (a shared hobby counts as a mutual friend). Everything else holds up.

Judged against:
- Engine: NetworkX in a long-lived API process, graph loaded at start-up (README.md); version not stated.
- Prod size, November 2026: 2.1 million users, 9 million friendships, 15 interests; `music` liked by about 1.3 million users, `cooking` by 700,000, the smallest interests a few thousand (README.md).
- Operation: `suggest(G, user)` on the home page "people you may know" box, interactive, budget 100 ms (README.md).
- Writers: `clubgraph.build.load` is the only writer; it puts friendships and interests in one undirected graph, edges tagged `friend` and `likes` (build.py).
- Sample: data/ has 3,000 users, 15 interests, 16,410 friendships, 5,226 likes; same shape as prod (README.md). Biggest interests in the sample: music 1,826, cooking 1,068, film 914.

## Findings

### critical: `suggest`
The people-you-may-know box is a tourist who is told "your neighbours' neighbours" and decides that the 1.3 million people who like music are all your neighbours' neighbours. Everyone who owns a pair of running shoes is now a "mutual friend". The ranking is a lottery with a hobby filter.
Problem: When `suggest` runs for a user who likes `music` on the prod data (1.3 million users like music, README.md), `for n in G[user]` includes `interest:music`, and `for m in G[n]` then visits all 1.3 million of those users and adds 1 to each score. That is millions of dictionary updates for one request, against a 100 ms budget, and the same happens for `cooking` (700,000). The scores are also wrong: an interest counts like a mutual friend, so people who merely share a hobby outrank or tie with real friends-of-friends. On the sample, 395 of 30,000 returned suggestions (10 each for 3,000 users) have no mutual friend according to `mutual_friends`, and for u00000 there are 1,206 candidates reached through interests against 139 through friends. `mutual_friends` itself checks `kind == "friend"`, so the file already knows the rule that `suggest` skips.
Fix: Follow only friend edges at both hops. In `suggest`, `if G.edges[user, n]["kind"] != "friend": continue` before the inner loop, and require `G.edges[n, m]["kind"] == "friend"` before scoring m. Work then drops to the friends' friends (about 8.6 friends per user and under a hundred candidates at 9 million friendships over 2.1 million users, derived from the README) and the scores are true mutual-friend counts. If interests should influence ranking, add them as a separate, bounded signal (for example, only interests with a few thousand likers), not as extra hops through the same loop. Check after the change: every suggestion has a non-empty `mutual_friends(G, user, m)`.

## Holds up
- `mutual_friends`: filters both sides on `kind == "friend"` and intersects, which is correct. It is cheap for any user (two neighbour lists). It is also the rule `suggest` should follow.
- `load`: one graph for both relationships is fine at this scale for a start-up-loaded, read-only graph; the edge `kind` attribute separates them. It is only a problem because `suggest` ignores it. Splitting interests into a separate structure would make this class of mistake impossible, but that is optional once `suggest` is fixed.
- Lookups by user id: nodes are keyed by id in NetworkX, so there is no index to miss.

## Not checked
- Prod timing was not run; the claim of millions of visits comes from the README's numbers and the loop structure. On the 3,000-user sample the call takes about 20 ms, which says nothing about 2.1 million users.
- NetworkX version is not stated; nothing here depends on it.
- `tests/test_suggest.py` builds a small graph with no interest nodes, so it passes without exercising the bug.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
