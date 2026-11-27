# Roast: wikiprune (archive selection)

Verdict: Not sound. Run as it is, the script would archive 53 pages where the README's rule gives 37. The 16 extra pages are reachable from the main wiki; the bug is in `clusters`, which follows links in one direction only. Fix `clusters` before the first Sunday run.

Judged against:
- README.md: "if A links to B, A and B are in the same cluster whoever links to whom"; a cluster of fewer than three pages gets archived.
- README.md: "Most content pages are reached from one of the index pages and have no links of their own."
- README.md: the archive bot moves every page in out/archive.txt on Sunday at 23:00.
- data/pages.csv: 420 titles, all distinct. data/links.csv: 611 links, every endpoint is in pages.csv.
- wikiprune/clusters.py: `MIN_SIZE = 3`; `clusters` walks `G.neighbors(p)` on a `nx.DiGraph`.

## Findings

### critical: `clusters`
Problem: When `archive_list` runs on the shipped data, `clusters` walks `G.neighbors(p)` of a directed graph, which returns only the pages a page links to. The README says links count in either direction. Pages are visited in sorted order, so a content page with no links of its own (for example `Astast`, linked only from `Briuv`) is visited before the page that links to it, becomes a one-page cluster, and is marked seen. The linking page then cannot reach it. The result is 50 clusters where the README rule gives 36, with the largest at 367 pages where the connected set is 380. 53 pages are archived; 16 of them are in the connected set and should not be. The trigger is the shipped data; the right answer is stated in the README; the wrong output is certain for this data because the visit order is fixed.
Fix: Walk the undirected view. In `clusters`, add `U = G.to_undirected(as_view=True)` before the loop and iterate `U.neighbors(p)` in place of `G.neighbors(p)`. Checked in memory, not written to the repo: the fixed logic archives 37 pages on this data, the same as `nx.weakly_connected_components` filtered to size below 3. Migration: none; the output file is rebuilt on each run.

### low: `test_two_islands`
Problem: The test passes with the bug because its chain `a -> b -> c` is visited from its source, which sorts first. No test has a page reached only by an in-link, so the failing shape is never run. Both existing tests pass on the current code (2 tests, OK).
Fix: Add a case that fails on the current code, such as `nx.DiGraph([("z", "a"), ("z", "b"), ("z", "c")])`, which should give no archived pages (currently it archives `a`, `b`, `c` and `z`). Expected result after the fix: `archive_list` returns `[]`.

### low: `archive_list`
Problem: Nothing checks the list before the bot reads it. A bad graph load or a future regression goes straight to the Sunday move with no count, no diff against the last run, and no dry run. This is insurance, not a defect in today's data.
Fix: Print the count and the titles that are new since the previous `out/archive.txt`, and require a manual confirmation or a sanity cap (for example, refuse to write if the count changes by more than a set percentage) before the bot's Sunday run.

### low: `load`
Problem: Link endpoints that are not in pages.csv are added as nodes by `add_edges_from`, so a mistyped title in links.csv would produce a page in archive.txt that does not exist. None of the 611 shipped links is affected (checked), so this is a question to confirm, not a current defect.
Fix: Confirm the loader for links.csv rejects titles missing from pages.csv. If it does not, raise an error in `load` when an endpoint is not in the page set.

## Holds up
- `clusters` visited-set logic (wikiprune/clusters.py): once the walk is undirected, the set bookkeeping is correct; the fixed version matches the weakly connected components on the shipped data.
- `MIN_SIZE = 3` with `len(group) < min_size` (wikiprune/clusters.py): matches the README's "fewer than three pages"; a three-page cluster is kept.
- `load` (wikiprune/wiki.py): reads pages and links with DictReader and UTF-8; the 420 titles are distinct and all link endpoints are present. Would change if titles differed only in case or whitespace across the two files; neither file shows that.
- `__main__` (wikiprune/__main__.py): creates `out/` and writes one title per line, as the README describes.

## Not checked
- The archive bot and its Sunday schedule are not in this repo; what the bot does with an unknown title was not checked.
- No network, no install. Logic was run in memory against the shipped CSVs. `out/archive.txt` was not written.
- The fix was run as a copy in memory, not applied to wikiprune/clusters.py.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
