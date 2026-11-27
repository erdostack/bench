Decision: in-process-library

The recorded decision was recursive-sql for the desk's own network (640 stations, about 9,800 sections). At national scale (2,600 stations, 380,000 sections) the recursive query measured 7.4 s p95 on your merged test copy, against the 1 s budget, so that decision no longer stands. Kofi's more cores is not a fix I can confirm: SQLite runs one statement on one thread, and nothing I ran tested it, so it does not reopen the query.

The change I recommend is to answer cut-offs from a structure built once per nightly export, not to run a walk per closure. A section closure only cuts stations off if that section is a bridge between the core network and them. Precomputing that per section takes about 1.6 to 1.7 s to build for 380,000 sections, and each answer is then a lookup of 0.5 to 4 microseconds. In a synthetic check of 13,838 single-section closures on small random networks, the lookup agreed with a brute-force walk every time; on the national-size synthetic graphs, three random closures per size also agreed.

What I measured here (synthetic, this machine, in memory, no files written):

- A plain per-closure walk over the whole network: p95 about 1.1 s at 150,000 track nodes and about 1.25 s at 300,000. That is at or over the budget, so the bare in-memory walk does not meet it on its own.
- The precomputed lookup: as above. Process peak about 170 to 250 MB, well inside the 8 GB box, one copy per process.

What I did not measure: the real track node count, core node count and topology (the synthetic graphs are random, and real networks have more branch lines); the nightly export window; and the real-file timings. The 7.4 s and the 2,600 and 380,000 figures are yours, not re-run here.

Before committing, run this on the merged file:

1. Time the nightly build of the cut-off structure, and check it fits the export window.
2. Check the lookup against the brute-force walk for about 20 random closures.
3. Time the lookup p95 and the process's memory on the 8 GB box.

If the build misses the window or the lookup is over 1 s, the next step is to measure the cores change on the merged file. A graph database is only worth considering if that fails as well, which this workload does not currently point to, because the network fits in one process and changes once a night.

Open questions for you: can two sections be closed at once? The lookup covers one closed section; a combined closure needs its own answer. Do the desk need answers on the live register during the day, not the previous night's export? Frequent changes would make the nightly rebuild too slow.

Changed in the repo: `docs/graph/DECISION.md` now has the new Decision line, with the national-scale facts beside the previous desk-network figures. Nothing else in the repo was changed, and `sql/cut_off.sql` is untouched.
