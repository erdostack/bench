# Roast: tram kiosk database (schema.sql and queries/)

Verdict: The slowness has one cause. `queries/fewest_stops.sql` walks every route on the network before it returns an answer, and on the 144-stop network that never finishes. The other two queries are bounded and fine. The fix is to precompute the answer nightly, which the kiosk refresh already does.

Judged against:
- 144 stops on twelve lines (T1 to T12), every link stored in both directions: README.md ("The network" section).
- Kiosks answer offline from a local SQLite copy, refreshed nightly, so every question is interactive and runs on the kiosk: README.md (first paragraph).
- Question 1, "How many stops to X?", runs `fewest_stops.sql` with `:from_stop` and `:to_stop`: README.md, queries/fewest_stops.sql.
- Question 2, "What's nearby?", runs `stops_within.sql` with `:n` = 1 or 2: README.md, queries/stops_within.sql.
- Line view runs `line_stops.sql`: README.md.
- Intended answer: "Fewest stops", and the walk "never revisits a stop": queries/fewest_stops.sql, first comment line.
- Shape of the data as measured: 420 directed links, 12 lines, degree 1 to 4, longest shortest route 22 hops (stop 144 to stop 14): tram.db (measured, not stated in the README).

## Findings

### critical: `queries/fewest_stops.sql`
Every kiosk asks this question, and it is the slow one. The walk has no depth limit, and the query only picks the shortest route after the whole walk has run. The grid gives it a lot of routes to visit.

Problem: When fewest_stops runs from any stop to another on the 144-stop network, the recursive walk generates every simple route out of :from_stop before ORDER BY hops LIMIT 1 can choose the shortest. Nothing bounds the depth. On tram.db, stop 144 to stop 132 (one hop apart) did not return within 20 s. Capping the walk at 22 hops alone produced 4,747,738 rows in about 12 s, and the uncapped walk keeps growing past that.
Fix: Stop searching at query time. In the nightly build, run a breadth-first search from each stop and store the result: `CREATE TABLE route (from_stop INTEGER NOT NULL REFERENCES stop(id), to_stop INTEGER NOT NULL REFERENCES stop(id), hops INTEGER NOT NULL, path TEXT NOT NULL, PRIMARY KEY (from_stop, to_stop)) WITHOUT ROWID;` (20,736 rows for 144 stops). The query becomes `SELECT hops, path FROM route WHERE from_stop = :from_stop AND to_stop = :to_stop;`. Migration: add the table to the nightly refresh, populate it from link, then ship the new query. Checked on SQLite 3.53.1 in an in-memory copy: the build takes about 0.08 s and the lookup uses the primary key.

### low: `link`
Problem: The README says every link is stored in both directions. All 420 rows in tram.db are symmetric today, but schema.sql does not enforce that. The REFERENCES clauses on from_stop and to_stop only take effect when a writer enables `PRAGMA foreign_keys`, which is off by default. The loader is not in the repo, so this is a question to confirm: does the refresh write both directions in one transaction, and does it enable foreign keys?
Fix: Confirm it in the loader. If it is not already guaranteed, write both directions in one transaction, and add a refresh check that counts links with no reverse row (the count is 0 on tram.db today).

## Holds up
- `queries/stops_within.sql`: the recursion stops after :n hops (the kiosk passes 1 or 2), and UNION collapses repeated (stop, hops) rows. Ran for n = 1 (2 rows) and n = 2 (5 rows), each in under 0.01 s. This would change if the kiosk ever passed a large n.
- `queries/line_stops.sql`: uses the `link_line` index (plan: SEARCH link USING COVERING INDEX link_line (line=?)). Ran for T1 and returned 20 stops in under 0.01 s. The from-side list matches the to-side list because links are symmetric. This would change if a line were loaded with one-way links.
- `link` primary key (from_stop, to_stop) with the `link_to` index: the walks read outwards by the primary key prefix (plan: SEARCH link USING PRIMARY KEY (from_stop=?)) and reverse lookups use the covering `link_to` index. Holds up for the current access pattern.

## Not checked
- The nightly loader and refresh script are not in the repo, so the two-way guarantee and the foreign key setting are unconfirmed.
- Only tram.db was run, on this machine and on SQLite 3.53.1 through Python's sqlite3. Kiosk hardware and kiosk SQLite version were not checked.
- No pair of stops was run to completion through fewest_stops.sql. Runs were stopped by a time limit; the full number of simple routes was not counted.
- The route table fix was checked in an in-memory copy only. The tram.db file was not changed.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
