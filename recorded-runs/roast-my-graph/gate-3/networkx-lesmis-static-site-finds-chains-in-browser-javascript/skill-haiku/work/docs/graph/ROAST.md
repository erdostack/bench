# Roast: barricade (site/path.js and the data it reads)

Verdict: Sound. The hand-written BFS in `site/path.js` is correct for this graph, and the review's must-fix is not needed. The only defect is a low-severity input bug (`shortestChain` throws on a few names that exist on every object), and it does not affect any chain the exhibition can show.

Judged against:
- Static site on GitHub Pages; the visitor's browser runs everything; no server and no Python at runtime. (README.md)
- Build step in CI: `scripts/export.py` writes `site/data/lesmis.json` and `site/data/check.json`; networkx is a build dependency only (`requirements-build.txt`, `networkx>=3.2`). (README.md; requirements-build.txt)
- Graph: 77 characters, 254 links, from `networkx.les_miserables_graph()`. (README.md) Checked in this review: 77 nodes, 254 undirected links, every adjacency entry is mirrored, and one connected component.
- Expected lengths: 60 random pairs computed with networkx; `node --test` checks `shortestChain` against them. (README.md; tests/path.test.mjs)
- Interactive: one lookup per submit, on a graph of 77 nodes. No rate or latency is stated.

## What the reviewer said, checked
- The reviewer's suggestion is to call `nx.shortest_path` "like export.py does". `scripts/export.py` does not call `nx.shortest_path`; it calls `nx.shortest_path_length` and stores only the lengths in `check.json`. Nothing in `export.py` builds a chain.
- networkx cannot run in the browser: the README says there is no Python at runtime. The only networkx code is the build step, which writes data and never answers a visitor's query.
- So the library call the reviewer means can only run at build time. If the page should use networkx's answers, the build would have to ship precomputed chains. For 77 characters that is 5,852 ordered pairs, and the BFS already gives the same lengths, which the tests confirm.

## Findings

### low: `shortestChain`
Every name in the exhibition passes the guard, and the only ones that break it are the ones every JavaScript object was born with, which is a fine bit of trivia for a visitor to be stuck on.
The guard `from in graph.adj` and `to in graph.adj` checks the prototype chain as well as the data, so names that every object has pass the guard.
Problem: When a visitor types `toString`, `constructor` or `__proto__` into either box, the guard passes, the loop calls `graph.adj[name]`, and the function throws `TypeError: graph.adj[name] is not iterable`. The page does not update and shows no message. Reproduced in Node 22.23.5 with this module and `lesmis.json`. The inputs are free text, so this is reachable; no real character has one of these names, so no correct answer is lost.
Fix: Use an own-property check: `if (!Object.hasOwn(graph.adj, from) || !Object.hasOwn(graph.adj, to)) return null;` (Object.hasOwn is in Node 16.9+ and current browsers). Add a test for `"toString"` returning `null`.

### low: `check.json`
The README says CI runs `scripts/export.py` to build both data files. No CI configuration is in the repo.
Problem: Nothing in the repo shows that the committed `check.json` and `lesmis.json` are regenerated from the current networkx. The test compares `path.js` with whatever `check.json` contains, so a changed export could leave the test checking old numbers. The files do not show this has happened.
Fix: Confirm the CI job runs `export.py` and fails on a diff. If there is no such job, add one that regenerates the data and checks `git diff --exit-code site/data`. Pinning networkx in `requirements-build.txt` (currently `>=3.2`, no upper bound) would also make regenerated data reproducible.

## Holds up
- `shortestChain` (`site/path.js`): an unweighted breadth-first search. It stops when `to` is dequeued, rebuilds the chain from `previous`, and returns `[from]` for the same character and `null` for an unknown name or an unreachable one. A shortest-path search needs nothing more than BFS on an unweighted graph, and the answer is the same lengths networkx gives, which the 60-pair test checks. The rewrite the reviewer asks for would produce the same output at build time, so it would not change what a visitor sees.
- The tests (`tests/path.test.mjs`): 3 of 3 pass in Node 22. The first test checks both the length and that every step is a real link, so a wrong chain would fail even with the right length.
- `site/data/lesmis.json`: 77 nodes, 254 links, symmetric, one connected component. It matches the README and the networkx figures.
- `site/index.html`: the datalist is built from the same adjacency, so the suggestions are the names `shortestChain` knows.

## Not checked
- The browser was not run. The prototype-key failure was reproduced with Node on the same module and data, not in a browser, and the page's own error handling was not observed.
- `scripts/export.py` was not run, and networkx was not available to check, so the committed data was checked only against the test and the README figures.
- No CI configuration exists in the repo, so whether the build runs and fails on drift is not checked.
- Which of several equally short chains the page shows is decided by the sorted adjacency order. The files do not say whether the exhibition expects a particular chain.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
