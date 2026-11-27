I added `recall_list(tube_id)` to `tubetrack/graph.py`, directly below the lineage code.

- It returns every tube derived from the recalled tube, directly or through later aliquots, extractions or pools. It returns them sorted, using the ids as written in `data/tubes.csv`. The recalled tube is not included.
- Input is matched case-insensitively and ignores surrounding spaces, because `derivations.csv` has ids like `bb-0045 ` and the lab may paste them in any form.
- An id that is not in `tubes.csv` raises `ValueError`, so a typo does not come back as an empty pull list.
- `lineage_plot_data` and `derivation_graph` are unchanged, so the lineage plots behave as before.

Checks: every tube in the export runs without error, no tube appears in its own list, and `lineage_plot_data` still returns results for the same inputs.

Things to decide before the lab uses this:
- The list includes tubes already marked `destroyed` or `shipped`. Across all recall lists, 468 destroyed and 169 shipped entries appear. I did not filter them, because "has to pull" could mean either. If destroyed tubes should drop out, that is a one-line filter on `tubes.csv` status.
- The largest recall list has 50 tubes. Some ids in `derivations.csv` only match `tubes.csv` after normalising case and spaces. The data is not cleaned, so this normalisation is what makes those rows work.
