# Roast: wikiprune (wikiprune/clusters.py, wikiprune/wiki.py, wikiprune/__main__.py)

Verdict: Do not let it run for real yet. `clusters` is supposed to find groups that are connected "in either direction" (README) but it only follows links forwards, so on the shipped data it lists 53 pages for archiving when the README's rule gives 37. 16 live pages would be moved to the Archive on Sunday night, 13 of them from the main 380-page cluster. One small change (the library's weakly connected components) fixes it.

Judged against:
- README.md: a cluster is pages connected through links "in either direction"; clusters of fewer than three pages are archived; the bot moves every page in `out/archive.txt` on Sunday at 23:00; most content pages are reached from an index page and have no links of their own.
- Engine/library: Python 3 with NetworkX (version not stated in the repo); the graph is built as an `nx.DiGraph` in `wikiprune/wiki.py`.
- Size (data/pages.csv, data/links.csv): 420 pages, 611 links, all distinct, no self-links, every linked title is a listed page.
- Operation: batch, runs once a week; first real run is the next one (user request).

## Findings

### critical: `clusters`
A graph that was told "direction does not matter" and then walked only downhill, like a hiker who insists the mountain has no other side.
Problem: When `archive_list` runs on data/links.csv, `clusters` calls `G.neighbors(p)`, which on a `DiGraph` returns only the pages `p` links to. Content pages have no links of their own (README), so they are visited as one-page groups before the index page that links to them is reached, and the index page never pulls them in because they are already in `seen`. I ran it on the shipped data: it returns 53 titles, but the README's rule (connected in either direction, fewer than three pages) gives 37. The 16 extra pages are live: 13 sit in the 380-page cluster (for example `Astast`, linked from `Briuv`; `Astin`, linked from `Mika-Lovo` and `Shura-Inqua`) and 3 form the three-page chain `Quara-Milo` -> `Tensen` -> `Astlo-Astvo`, which is a three-page cluster and must be kept. The bot moves whatever is in the file, with no review step.
Fix: Use the library call instead of the hand-written walk (checked on the shipped data: it gives 37 titles, the correct list, and the same function on a small test graph gives the right answer):
```python
import networkx as nx

def clusters(G):
    """Every cluster of linked pages, as a list of sets of titles."""
    return [set(c) for c in nx.weakly_connected_components(G)]
```
`archive_list` stays as it is. The bundled tests pass either way, because both use chains whose link direction matches title order (`a`->`b`->`c`, `x`->`y`), the only shape the forward-only walk gets right; a graph with `b`->`a` and `b`->`c` already returns all of `a`, `b`, `c` from `archive_list`. Add tests where direction and title order disagree, and one that runs `load()` on data/ and expects the 37 titles. If you would rather keep the loop, iterate over `G.to_undirected(as_view=True).neighbors(p)`, but the library call is the fix.

## Holds up
- `load` (wikiprune/wiki.py): adds every row of data/pages.csv as a node and every row of data/links.csv as a directed edge; on the shipped data there are no links to unlisted titles (which would silently create extra pages), no duplicate titles and no self-links. Keeping the graph directed is fine for the library call above; direction is only wrong in `clusters`.
- `clusters` termination: the `seen` set and the `group` check stop the walk, so a loop of links cannot make it run forever. Only the direction of the walk is wrong.
- `archive_list`: the size test and the sorted output are right once `clusters` is right; a sorted list also makes the output stable between runs.
- `wikiprune/__main__.py`: writes one title per line, UTF-8, and reports how many were listed. The file is rewritten on each run; nothing in the files shows a partial write or a stale file causing a problem, so nothing to fix.

## Not checked
- The NetworkX version is not stated in the repo; the library call used is `nx.weakly_connected_components`, which I ran on the installed NetworkX.
- Whether the bot or a person reviews `out/archive.txt` before Sunday 23:00: not stated. If nobody does, check the 53-title output against the 37 above before the first real run.
- `out/archive.txt` was not created: the script was not run through `__main__`; the list was computed by calling `archive_list` directly.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
