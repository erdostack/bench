No, the page cannot be trusted. Verdict: critical.

Every bond it prints is "1 chapters together", whatever the real count. The cause is one line in `load` (studyguide/bonds.py): it uses a plain `nx.Graph()`, which keeps only one link per pair of characters, so the 820 rows of your chapter log collapse to 254 links and every bond becomes 1. I ran it. The "ten strongest bonds" are just the first ten pairs in alphabetical order (Anzelma and Eponine, Anzelma and MmeThenardier, Babet and Brujon, ...). The real top three are Cosette and Valjean (31 chapters), Cosette and Marius (21) and Marius and Valjean (19).

The "screen partners" numbers are wrong for the same reason: they count how many different people a character met, not chapters. Valjean shows 36 and should be 158, Cosette shows 11 and should be 68.

The fix is small: use `nx.MultiGraph()` in `load` and list each pair once in `strongest_bonds` (exact lines in docs/graph/ROAST.md). I checked the corrected numbers in memory on your data; I did not edit the files. The tests pass today only because they build their own tiny graph and never load the real log, so I recommend adding a test on the real data (Cosette and Valjean should be 31).

One low question: after the fix, three pairs tie at 12 chapters for the last two places, so one (Thenardier and Valjean) is dropped by alphabet. Decide whether that is acceptable.

Files: docs/graph/ROAST.md and findings.json (repo root, 4 findings).
