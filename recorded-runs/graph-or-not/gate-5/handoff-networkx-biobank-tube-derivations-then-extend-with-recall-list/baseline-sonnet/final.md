`recall_list(tube_id)` is now in `tubetrack/graph.py`, below `lineage_plot_data`.

- **What it returns:** every descendant of the tube through aliquots, extractions and pools, as a sorted list of ids written the way `tubes.csv` writes them (`BB-0123`). The recalled tube is not in the list.
- **Id forms:** the LIMS B rows in `derivations.csv` are lower case and some have trailing spaces. The function normalizes both the export and the id you pass in, so `bb-0020`, ` BB-0020 ` and `BB-0020` all give the same answer.
- **Destroyed tubes:** they are left off the list, but anything made from them stays on it. That is the rule `tubetrack/tools.py` already had, and I kept it.
- **Where the code lives:** `recall_list` already existed in `tools.py`. I moved it to `graph.py` and `tools.py` now just re-imports it, so existing callers still work.
- **Unknown ids:** an id that is not in `tubes.csv` now raises `ValueError`. The old version returned `[]`, which would look like "nothing to pull" if someone mistyped the id. A real tube with no descendants still returns `[]`.
- **Lineage plots:** `derivation_graph` and `lineage_plot_data` are untouched. I called `lineage_plot_data('BB-0034')` and it gives the same output as before.
- **Checks:** I ran it by hand against the current export, including lower-case and padded ids, an unknown id, and `tools.recall_list`. There is no test suite in the repo and I did not add one.

One thing to know: `lineage_plot_data` does not normalize ids, so it misses any tube whose id was exported in lower case. I left that alone because you asked for the lineage plots to keep working as they are.
