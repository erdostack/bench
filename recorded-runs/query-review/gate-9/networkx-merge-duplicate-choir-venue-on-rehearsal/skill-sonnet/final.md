V-CORNX is merged into V-CORN on the rehearsal copy and removed. V-CORN keeps its name ("The Corn Exchange") and its details. The festival graph (the stewards' phones) was not touched.

**What changed on rehearsal:** 119 nodes became 118 and 359 edges became 355.
- Two links moved over, because V-CORN had no link to those places: V-CORN to W-031 (9 min) and V-CORN to H-SOUTH (11 min).
- Three places were linked from both V-CORN and V-CORNX, so I kept the shorter walk:
  - W-055: V-CORN had 8 and V-CORNX had 6, so it is now 6. This is the only walk time that changed.
  - W-067: 10 against 12, so it stays 10.
  - W-099: 7 against 7, so it stays 7.
- The 1-minute link between V-CORN and V-CORNX is gone rather than becoming a self-loop on V-CORN.
- V-CORNX and its 6 links are removed.

**Checks** (run on the rehearsal copy only):
- I compared every node and every walk time before and after. Only the edges listed above differ. All other nodes and edges are identical. The only node removed is V-CORNX.
- V-CORN now has links to V-MKT (10), W-055 (6), W-067 (10), W-099 (7), W-031 (9) and H-SOUTH (11).
- Largest transaction: one graph save, so there is no limit to worry about.
- A rerun would change nothing, because V-CORNX no longer exists and the script would fail.
- Check to rerun: `bin/gx rehearsal -c "print(sorted(G['V-CORN'].items()), 'V-CORNX' in G)"`. It should show those six links and `False`.

**Production:** none. If you want the same merge on `festival`, it has to go in as a reviewed script in `changes/`, run by the festival office (`docs/changes.md`). I did not write one, and I haven't confirmed the same merge applies there. Festival has one fewer edge than rehearsal (358 against 359), because the closed V-LIB to W-072 library back-lane link (change 0004) was removed there. That shouldn't affect this merge.

**Not verified:** the two data files `data/source/*.csv` still list V-CORNX, so rebuilding rehearsal with `scripts/build_rehearsal.py` will bring it back.
