Done on the scratch copy. All 28 fixtures that were fed by DR-3 (F-0071 to F-0098) now feed from DR-5, each on its original circuit (21 to 48). Nothing else changed.

**Target**: scratch (`data/scratch-rig.json`), run with `bin/rig scratch run scripts/move_dr3_to_dr5.py`. The plan (`data/hallb-rig.json`) is untouched; its checksum still matches.

**Rule**: every `fed_by` edge whose rack is DR-3 moves to DR-5 with its `circuit` attribute kept. Sources: your request, and `docs/plan.md` (DR-5 uses circuits 1-20, DR-3's fixtures are on 21-48, so they keep their numbers without a clash).

**Numbers**:
- should change: 28 (counted from the graph before the run)
- job changed: 28 `fed_by` edges removed from DR-3 and added to DR-5
- same rows: yes (fixtures, circuits and destinations diffed against the plan)
- other rows or tables changed: 0 (`on_universe`, `powered_from` and `sends_data` edges identical to the plan; node set identical)
- DR-5 now has circuits 1-48, all in use
- DR-3 has no fixtures left; it keeps its `powered_from` edge to DISTRO-A and its `sends_data` edge from SPLIT-1, since you asked for nothing else to change

**Check to rerun**: count `fed_by` edges into DR-3 in the scratch file (should be 0), and into DR-5 (should be 48: the 20 that were already there plus the 28 moved, one per circuit 1-48).

**Production**: none. The plan file was not changed.

**Not verified**: nothing else. The script is at `scripts/move_dr3_to_dr5.py` in the working directory.
