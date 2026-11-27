I wrote `cut_off(conn, down_station)` in `linewatch/shutdown.py`. It follows the recorded decision in `docs/graph/DECISION.md`: one recursive query on the SQLite layout file, with no networkx and no Neo4j.

- **What it returns:** the sorted ids of stations that can reach a dock today but cannot once `down_station` is out. `down_station` itself is never listed.
- **Line engineering's rule:** it walks backwards from the docks along segments in their direction, and bypass segments are ignored. If the station taken out is a dock, it stops counting as a dock.
- **Already-stranded stations:** stations that can't reach a dock even with everything running are not listed, because this shutdown doesn't cause that. This follows the baseline note in the decision record. If you want them reported separately, that's an easy addition.
- **How it runs:** two statements per check, one with the station out and one without. Each statement touches each station at most once. The record's synthetic run (640 stations, 1,500 segments) took about 1.4 ms per check.
- **Testing:** I tried it on a small in-memory database built from `db/schema.sql`. It covered:
  - a station with a second route (not cut off);
  - a bypass-only link (ignored);
  - a station already stranded (not listed);
  - a dock going down (the stations behind it are listed);
  - an unknown station id (`[]`).
- **Not done:** I didn't add a test file, and I didn't run it on the real `var/layout.db`, because it isn't in the repo.
- **Left unchanged:** the record proposes `CREATE INDEX segment_to_idx ON segment(to_station)`. I didn't add it to `db/schema.sql`, because line engineering keeps that file, so someone should add it. I also left `linewatch/reach.py` alone. It's unused, and it takes both directions and counts bypass segments, so it shouldn't be used for this.
