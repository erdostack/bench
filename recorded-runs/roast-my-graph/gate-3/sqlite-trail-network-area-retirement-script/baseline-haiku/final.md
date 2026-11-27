The quarry is still routable because retiring it deleted the junctions but not the segments that point at them. The retire script is the root cause, and the planner makes it worse by trusting the segment table alone.

What's wrong, most serious first:

1. **The retire script never cascades (scripts/retire_area.py, retire, critical).** `retire()` opens its own connection and never sets `PRAGMA foreign_keys = ON`. SQLite has foreign keys off by default, so the `ON DELETE CASCADE` in db/schema.sql does nothing. The script deletes the quarry's 60 junctions, leaves their segments in place, writes the retired_area row, and reports success. This is what happened in September.

2. **The planner routes through retired junctions (app/routes.py, load_graph, critical).** `load_graph` builds the graph from the segment table without joining to junction. On trails.db, 153 of 300 random pairs of live junctions produce a route through a retired junction. One example runs 69 to 352 through quarry ids 169, 121 and 238. Six surviving segments link the quarry chain to live junctions, which is how the planner gets in.

3. **90 orphan segments are left in the data (segment, high).** 84 have both ends in the quarry, and 6 join it to the live network. Foreign keys are off, so nothing flags them. The table needs a one-time cleanup, after you confirm the count.

4. **The planner hides the problem (app/routes.py, plan, medium).** `names.get(j, f"junction {j}")` turns a missing junction into a placeholder name, so a route through a closed area still comes back looking valid. Unknown start or end ids also raise unhandled networkx errors.

5. **Nothing reads retired_area (retired_area, medium).** The table is written and never checked, so a closure record has no effect on routing.

6. **Typos are recorded as closures (retire, medium).** An area name with a typo deletes 0 junctions, prints a success line, and still writes a retired_area row.

7. **Relative database path (DB and DB_PATH, low).** Running the script from another directory creates an empty trails.db there.

What to do, in order:
- Make the retire script use `app.db.connect()`, or set the pragma itself. Make the script refuse a name with no junctions, and roll back if any segment is left pointing at a missing junction.
- Delete the 90 orphan segments once, after checking the count, then run `PRAGMA foreign_key_check` to confirm it is clean.
- Change `load_graph` to join both endpoints to junction. Make `plan()` fail loudly on a missing junction.
- Add a test that retires a small fixture area and checks its segments are gone and that no route passes through it.

The sample numbers come from read-only queries and an in-memory copy of trails.db on this machine. I did not change the database. Full list with fixes: /run/work/findings.json
