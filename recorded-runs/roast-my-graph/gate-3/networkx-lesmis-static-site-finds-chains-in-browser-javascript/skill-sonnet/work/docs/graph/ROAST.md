# Roast: barricade/ (Les Mis character-chain site)

Verdict: Nothing serious, and no, you do not have to replace `site/path.js` with `nx.shortest_path`. The site is static and runs in the visitor's browser with no Python at runtime, so NetworkX cannot be called there; `shortestChain` is a small, correct breadth-first search, and `scripts/export.py` already uses `nx.shortest_path_length` where Python does exist, at build time, to check it. The one thing I would fix is a `low` crash on a few odd typed names.

Judged against:
- Runtime: static site on GitHub Pages, runs entirely in the browser, no server and no Python at runtime (`README.md`).
- Size: 77 characters and 254 links, NetworkX's bundled `les_miserables_graph()` (`README.md`; the exported `site/data/lesmis.json` has 77 nodes and 254 undirected links, which I checked).
- Operation: a visitor picks two characters and the page shows the shortest chain of co-appearances; the weights on the NetworkX edges are not used (`README.md`, `site/path.js`). Traffic: not stated.
- Tests: `node --test` on Node 20+, comparing chain lengths to `site/data/check.json`, 60 random pairs computed by NetworkX (`README.md`, `tests/path.test.mjs`).

## Findings

### low: `shortestChain`
The graph is fine; the lookup treats the word "constructor" as a character.
Problem: When a visitor types a name that is a property every JavaScript object has (`constructor`, `toString`, `__proto__`) as the first character, `from in graph.adj` is true because `in` also sees inherited properties, so the search starts and `for (const next of graph.adj[name])` throws `TypeError: graph.adj[name] is not iterable`. The submit handler in `site/index.html` then throws and the page shows nothing. I ran it and got the TypeError for all three. As the second name these return `null` and the normal "Pick two characters from the list." message. No wrong chain is ever shown; this needs a visitor to type one of those words.
Fix: Test own properties only: `if (!Object.hasOwn(graph.adj, from) || !Object.hasOwn(graph.adj, to)) return null;` (Node 16.9+ and current browsers).

## Holds up
- `shortestChain` (the hand-written BFS): correct for this graph. The graph is undirected with every link listed from both ends (checked: no asymmetric, duplicate or self links), BFS on an unweighted graph gives the fewest links, it marks nodes when they are queued so it cannot loop, and it returns `null` for unknown or unreachable names and `[from]` for the same character. I compared its chain length with an independent BFS for all 5,929 ordered pairs of the 77 characters: no differences. Calling `nx.shortest_path` is also not possible here: there is no Python in the browser, and the alternative (shipping a Python runtime to the page) would trade 20 lines for a very large dependency. If the reviewer wants parity with NetworkX, `tests/path.test.mjs` already checks it against NetworkX output on 60 pairs.
- `export.py`: `nx.shortest_path_length(G, a, b)` is unweighted, the same hop count the page computes, even though the NetworkX edges carry weights of 1 to 5 (co-appearance counts), which the README says are not part of the question. The seeded `random.Random(1832)` keeps `check.json` stable. I recomputed all 60 lengths with NetworkX and they match, and `lesmis.json` equals the NetworkX adjacency.
- `site/data/check.json` / `tests/path.test.mjs`: the test asserts the right things (length equals NetworkX's, both ends correct, every step is a real link). The graph is connected, so the unreachable-pair case does not occur in the data.

## Not checked
- Behaviour in real browsers and on the deployed Pages site; I ran `node --test` (3 of 3 pass) and the function under Node 22.
- Site traffic and any accessibility or UI review: out of scope for a schema and query roast.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
