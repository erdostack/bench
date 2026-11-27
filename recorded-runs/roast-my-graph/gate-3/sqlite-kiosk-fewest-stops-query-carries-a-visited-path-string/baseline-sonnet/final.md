The kiosks are slow because of one query: `queries/fewest_stops.sql`. It never finishes on this network.

**Why it hangs.** The recursive query builds every possible route from the start stop and only picks out the ones that end at the target afterwards. The only rule is that a single route can't revisit a stop. Your network is a grid of 144 stops on 12 crossing lines, so the number of distinct routes is astronomically large. The `ORDER BY hops LIMIT 1` at the end can't cut it short, because SQLite has to build all the routes before it can sort them. I ran it against a copy of `tram.db` and it was still going after 10 seconds, even for a stop one hop away (1 to 13). Every other pair I tried did the same. The `path` string it carries (searched with `instr()` on every step) makes each route unique, so nothing can be collapsed.

**Fix.** Search outward one hop at a time and track only the stop and the hop count, not the route:

```sql
WITH RECURSIVE walk(stop, hops) AS (
  SELECT :from_stop, 0
  UNION
  SELECT l.to_stop, w.hops + 1 FROM walk w JOIN link l ON l.from_stop = w.stop
  WHERE w.hops < :max_hops
)
SELECT MIN(hops) FROM walk WHERE stop = :to_stop;
```

On the copy this takes about 0.05 s per query (1 to 13 is 1 hop, 1 to 2 is 3, 1 to 100 is 11). Always pass a depth cap; 143 is the ceiling for 144 stops. If the kiosk needs the actual route and not just the stop count, rebuild it in the app from a parent per stop rather than carrying the route in each row.

**The rest is minor.**
- `stops_within.sql` is fine. It collapses duplicates and is bounded by `:n`.
- `line_stops.sql` builds two temporary sorts but only works with 28 to 42 links per line, so it isn't a problem today.
- The `link_to` index isn't used by any query, so it costs space and rebuild time for nothing.
- The `link_line` index is used by `line_stops.sql` but barely helps at 420 rows.
- The primary key on `link` allows only one line per pair of adjacent stops.
- `link.line` has no constraint on its values.
- The foreign keys are only enforced if the connection turns them on. There are no orphan links in the data.

The full list, with severity and fixes, is in `findings.json` in the repo root.
