No, do not use the "strongest bonds" page yet. It gets the main numbers wrong.

- Every bond on the page shows 1 chapter. The data has 31 shared chapters for Valjean and Cosette, for example, but the code keeps only one. The "top ten" are just the first ten pairs in alphabetical order (Anzelma and Eponine, Anzelma and MmeThenardier, and so on).
- The "screen partner" totals count how many people a character shares a chapter with, not how many chapters. Valjean's total reads 36; from the file it is 158.

The data file itself is fine: it matches the Les Misérables weights bundled with NetworkX for all 254 pairs. The fault is in the loader in studyguide/bonds.py, which keeps one row per pair instead of counting them. The fix is a few lines there, and the expected top three are Valjean and Cosette (31), Marius and Cosette (21), and Marius and Valjean (19). The tests also missed this because they never load the real rows, so they should be extended as well.

Files:
- /run/work/findings.json
- /run/work/docs/graph/ROAST.md
