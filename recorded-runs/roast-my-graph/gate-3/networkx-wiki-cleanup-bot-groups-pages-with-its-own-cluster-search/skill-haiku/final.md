Roast: wikiprune (archive selection)

Verdict: Not sound. Run as it is, the script would archive 53 pages where the README's rule gives 37. The 16 extra pages are reachable from the main wiki. The cause is in `clusters`, which follows links in one direction only. Fix it before the first Sunday run.

Findings (worst first):
- critical: `clusters`. It walks outgoing links only, so a page that is linked from another page but has no links of its own can end up as a one-page cluster and be archived. Fix: walk the undirected view (`G.to_undirected(as_view=True)`). In memory this gives 37 pages on the shipped data, the same as the README rule.
- low: `test_two_islands`. It passes on the buggy code and never covers an in-link. Add a case such as `z -> a, z -> b, z -> c`, which the current code archives and the fixed code does not.
- low: `archive_list`. No count or diff check before the bot reads the file. Insurance only.
- low: `load`. A mistyped link title would become a nonexistent archived page. None of the shipped links is affected; confirm the loader rejects them.

Not run: the fix was tested in memory on a copy and not applied to the repo. `out/archive.txt` was not written. The archive bot itself is not in this repo.

Files:
- /run/work/docs/graph/ROAST.md
- /run/work/findings.json
