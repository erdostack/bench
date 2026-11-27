I added `recall_list(tube_id)` to `tubetrack/graph.py`, next to the lineage code. I followed the recorded decision in `docs/graph/DECISION.md` (in-process networkx, no Neo4j), so I didn't re-decide anything and left that file alone.

- **What it returns:** the sorted ids, as written in `data/tubes.csv`, of every descendant of the recalled tube through any number of aliquots, extractions and pools. The recalled tube itself is not included.
- **Destroyed tubes:** they are left off the list but still walked through, so anything made from them before they were destroyed stays on it. Shipped tubes stay on the list, as the recorded rule says.
- **Ids in any form:** ids are stripped and upper-cased (new `normalize_id`) in both the input and the derivation graph. LIMS B's lower-case or trailing-space ids therefore join up with the main lab's chains. An id that is in neither the derivations nor `tubes.csv` raises `KeyError`. A tube with no descendants returns `[]`.
- **Lineage plots:** unchanged. `derivation_graph()` takes a new `normalize` flag that defaults to off, so `lineage_plot_data` gives the same output as before. I checked it on `BB-0091`.
- **Lineage bug left as is:** the lineage plots still treat a LIMS B id and its upper-case twin as two tubes, which breaks chains between the labs. I didn't change that because you asked for the plots to keep working as they are. Passing `normalize=True` there would fix it if you want it.
- **Checks:** I tried it on the 600-tube sample in `data/`. The largest recall, `BB-0086`, has 50 descendants and 41 after dropping destroyed tubes. A lower-case id with spaces around it gives the same result as the clean one. I didn't write a test file.
- **Open question for the lab manager:** whether shipped tubes should be pulled. I kept them on the list.
- **Not covered:** the full 18,400-tube export, which isn't in the repo. A derivation cycle in it wouldn't break the walk, but I haven't seen the full data.
