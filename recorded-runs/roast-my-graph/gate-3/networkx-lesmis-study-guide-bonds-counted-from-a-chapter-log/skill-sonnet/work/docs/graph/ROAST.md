# Roast: studyguide/ (the "strongest bonds" page)

Verdict: No, the page cannot be trusted. Every bond it prints is 1 chapter, whatever the real count, so "strongest bonds" is a list of arbitrary pairs in alphabetical order and the screen-partner totals are just numbers of friends. The cause is one line, and the fix is small.

Judged against:
- Engine: NetworkX, in-process, Python 3.13 (README.md); no `docs/graph/CONTEXT.md`.
- Data: `data/shared_chapters.csv` is "one row for every chapter in which two characters both appear", so a pair sharing 12 chapters has 12 rows (README.md). I counted 820 rows for 254 distinct pairs.
- Meaning: "Bond between two characters = the number of chapters they share" (README.md; `bond` docstring).
- Use: `python3 -m studyguide` prints the ten strongest bonds and the screen partners of six main characters, run on demand (README.md, `studyguide/__main__.py`).

## Findings

### critical: `load`
Les Misérables, 820 rows of chapters, and the graph went home with a single sticky note per pair: "they know each other". Valjean and Cosette spent 31 chapters together; the page says 1, the same as Valjean and a woman called Woman1.
Problem: When `load` runs on `data/shared_chapters.csv`, where `Cosette,Valjean` appears 31 times, it adds each row to an `nx.Graph()` with `add_edge`; a plain `Graph` keeps one edge per pair, so the 820 rows collapse to 254 edges and `bond` (`G.number_of_edges(a, b)`) returns 1 for every pair that appears at all. I ran the shipped code: every line of "Strongest bonds" says "1 chapters together" and the ten are the first ten pairs in alphabetical order (Anzelma and Eponine, Anzelma and MmeThenardier, Babet and Brujon, ...), while the true strongest are Cosette and Valjean (31), Cosette and Marius (21), Marius and Valjean (19). Every bond on the page is wrong, so this is the whole page.
Fix: Build a multigraph so that each row stays a separate edge: in `load`, replace `G = nx.Graph()` with `G = nx.MultiGraph()`. `bond` then returns the real count, because `number_of_edges(a, b)` counts parallel edges on a MultiGraph. `strongest_bonds` must then list each pair once, since `G.edges()` now repeats a pair once per chapter: change `pairs = sorted((min(a, b), max(a, b)) for a, b in G.edges())` to `pairs = sorted({(min(a, b), max(a, b)) for a, b in G.edges()})`. I ran this change on the shipped data without editing the files: top ten become Cosette and Valjean 31, Cosette and Marius 21, Marius and Valjean 19, Courfeyrac and Enjolras 17, Javert and Valjean 17, Combeferre and Enjolras 15, Combeferre and Courfeyrac 13, MmeThenardier and Thenardier 13, Bossuet and Courfeyrac 12, Gillenormand and Marius 12. Alternative: keep the plain `Graph` and add 1 to a `weight` attribute on each repeated pair, then read the weight in `bond`.

### high: `screen_partners`
A character's "screen partners" score is currently just how many different people they ever met.
Problem: `screen_partners` sums `bond` over the neighbours, and `bond` is always 1 (the finding above), so the page prints the number of distinct partners, not the total chapters: Valjean 36, Javert 17, Cosette 11, Marius 19, Fantine 15, Thenardier 16. The totals by the README definition are Valjean 158, Javert 47, Cosette 68, Marius 104, Fantine 47, Thenardier 61 (counted from the CSV). The ranking changes too: Cosette looks like the least connected main character and is third by real total. The function itself is right (it sums the bond over neighbours); it fails because of `load`.
Fix: No change in `screen_partners` itself once `load` is fixed; with the MultiGraph it returns the totals above (I ran it). Rated `high` and not a second `critical` only because it is the same cause.

### high: `test_bond`
The tests pass, which is the most suspicious sentence in this repo.
Problem: `tests/test_bonds.py` builds its own graph with `nx.Graph([...])` and never goes through `load`, so it can never see the collapse: `test_bond` asserts a bond of 1 on a pair that appears once, `test_partners` asserts 2 for two neighbours that appear once each, and `test_strongest_length` checks only the length. All three tests pass on the broken code (3 tests, OK) and would still pass after the fix. Nothing tests a repeated pair, which is the case that matters.
Fix: Add a test that loads the real data and checks a known count: `G = load(); self.assertEqual(bond(G, "Cosette", "Valjean"), 31)` and `self.assertEqual(strongest_bonds(G, 1)[0], ("Cosette", "Valjean", 31))`, and one with a repeated pair in a small `nx.MultiGraph`, e.g. `self.assertEqual(bond(M, "Cosette", "Marius"), 2)` with the edge added twice.

### low: `strongest_bonds`
Ten places, eleven contenders, and alphabet decides.
Problem: Three pairs tie at 12 chapters (Bossuet and Courfeyrac, Gillenormand and Marius, Thenardier and Valjean) for the last two places of the ten. `sorted(..., key=lambda t: -t[2])[:k]` keeps the alphabetical order of equal scores, so Thenardier and Valjean (12 chapters) is cut and the other two stay. After the fix the page silently omits an equally strong bond. A question to confirm: is a cut at a tie acceptable for the study guide?
Fix: If not, after sorting keep every pair whose score equals that of the k-th place (the page then has 11 rows), or print a note that ties were cut.

## Holds up
- `DATA`: the path is resolved from the file's own location, so `python3 -m studyguide` works from any directory.
- `load`'s CSV reading: `csv.DictReader` with the two named columns, correct for the two-column file (every row has two fields; no self-pairs found).
- `bond` and `screen_partners` as written: each does what its docstring says once the graph keeps repeated pairs; the wrong numbers come from `load`.
- `MAIN` in `studyguide/__main__.py`: a plain list of six names, all present in the data.

## Not checked
- The CSV's agreement with the chapter log in the book: only its internal consistency (820 rows, 254 pairs) was checked, and the README says it was written out from NetworkX's copy of Knuth's data.
- Whether the printed names (for example "MmeThenardier", "Gillenormand") are what the guide should show: not stated.
- I did not edit studyguide/ or the tests; the fix was run in memory only.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
