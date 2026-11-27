# Roast: studyguide (strongest-bonds page)

Verdict: No, the page cannot be trusted as it is. Every bond comes out as 1 chapter, so the "strongest bonds" list is just the first ten pairs in alphabetical order, and the screen-partner totals count people, not chapters. The data file is correct; the bug is in how `load` reads it.

Judged against:
- The chapter log has one row for every chapter in which two characters both appear, so a pair sharing 12 chapters has 12 rows; a bond is the number of chapters two characters share (README.md, lines 5-8).
- The page shows the ten strongest bonds and each main character's total bond with everyone else (README.md, lines 9-10; studyguide/__main__.py, lines 3, 8-12).
- The data file has 820 rows, 254 distinct pairs, 77 characters, and no self-pairs (data/shared_chapters.csv, lines 1-821). Its per-pair counts match the bundled Les Misérables weights in NetworkX exactly (checked read-only against `networkx.les_miserables_graph()`, networkx 3.7).

Measured (read-only, Python 3.13, networkx 3.7): the current code returns `('Anzelma', 'Eponine', 1)`, `('Anzelma', 'MmeThenardier', 1)` and so on for the top ten, all with bond 1. Valjean's screen-partner total is 36 (correct from the rows: 158). Javert gives 17 (correct: 47), Cosette 11 (correct: 68), Marius 19 (correct: 104), Fantine 15 (correct: 47), Thenardier 16 (correct: 61).

## Findings

### critical: `load`
The log has every shared chapter, and the loader throws all but one away.
Problem: `load` builds an `nx.Graph` and calls `add_edge` once per row. A simple graph holds one edge per pair, so the repeated rows for a pair collapse into a single edge. Every bond is then 1, and every total in `screen_partners` counts distinct people rather than chapters. For example, the file has 31 rows for Valjean and Cosette, and the page reads 1. The result is wrong on the main page, every time it runs.
Fix: Count the rows instead of collapsing them. In `load`: if `G.has_edge(a, b)`, add 1 to `G[a][b]["weight"]`; otherwise `G.add_edge(a, b, weight=1)`. In `bond`: `return G[a][b].get("weight", 1) if G.has_edge(a, b) else 0`. `strongest_bonds` and `screen_partners` then work unchanged. Expected output from the file: Valjean and Cosette 31, Marius and Cosette 21, Marius and Valjean 19, and screen partners Valjean 158, Marius 104, Cosette 68. No migration is needed, since the data is not stored anywhere else.

### low: `strongest_bonds`
Ties are broken alphabetically, so the list can look more exact than it is.
Problem: The sort is stable and only ranks by bond. After the fix to `load`, several pairs tie at 17, 13 and 12 chapters, and the cut at ten is decided by alphabetical order. The page does not say so.
Fix: Print the tie, or show "tied" beside pairs with equal bonds at the cut-off, so readers do not take the tenth place as a ranking.

### medium: `BondTest`
The tests cannot see the bug that shipped.
Problem: The tests build a `nx.Graph` by hand with one edge per pair, so they never pass repeated rows through `load`. Every assertion holds when each bond is 1, which is what the broken code returns, so the suite passes.
Fix: Add a test that calls `load` on a small CSV with two rows for one pair and expects `bond` to return 2, and a test that `screen_partners` counts chapters. Tests should use rows, not hand-built graphs, for `load`.

## Holds up
- data/shared_chapters.csv: the file is complete and matches the NetworkX Les Misérables weights exactly for all 254 pairs, so the bad totals are not caused by the data.
- `strongest_bonds`: the pair ordering (`min`, `max`) gives each pair one spelling, so `Valjean, Cosette` and `Cosette, Valjean` are not counted separately.
- `MAIN` in studyguide/__main__.py: all six names exist in the data.

## Not checked
- The page was not generated into the repo; the output above comes from calling the functions directly with the same arguments the page uses.
- Whether the chapter log is the right source for a study guide is outside these files and was not judged.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
