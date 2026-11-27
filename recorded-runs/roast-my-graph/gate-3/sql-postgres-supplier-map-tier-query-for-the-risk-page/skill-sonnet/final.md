The spinning is `queries/upstream_tiers.sql`. It's a recursive query that never stops on a loop, and your supply graph is full of loops.

The CTE `upstream` carries `tier` and `path` and joins with `UNION`. `UNION` only drops rows that are identical in every column, and `tier` and `path` change on every lap. So a ring such as the resin maker and the packaging firm is never recognised, and the walk keeps going until the connection is killed. I ran it on PostgreSQL 16.15 to confirm:
- **Small ring:** a 4-company ring with a 5 s `statement_timeout` timed out.
- **README scale:** 14,000 companies and 90,000 random links timed out at 20 s. The links were synthetic, because the real database isn't in the repo.

Even without loops, it enumerates every path rather than every company.

Rated critical. The fix replaces the cause with a breadth-first walk that visits each company once at its lowest tier. A plain recursive CTE can't do that, because it can't see rows from earlier laps. So it's a small plpgsql function, `upstream_tiers(plant bigint)`, in `findings.json` and `docs/graph/ROAST.md`:
- On the same 14,000/90,000 data it returned 13,974 companies in about 180 ms.
- Tiers matched a reference walk exactly.
- Every returned path was valid.

Then `app/risk_page.py` just calls `SELECT * FROM upstream_tiers(%(plant_id)s)`. There is also a quick stopgap (`UNION ALL`, a tier cap of 6 and PostgreSQL's `CYCLE` clause). It ran in 274 ms on the same data, but it still enumerates every simple path up to the cap and drops companies deeper than it.

One `low` note: `upstream` in `app/risk_page.py` has no statement timeout. That's why you see a hang rather than an error. Add `SET LOCAL statement_timeout = '5s'` and show an error on timeout.

The rest is fine. The indexes match the queries, and `flagged_suppliers.sql` and `direct_suppliers.sql` are fine.

I couldn't see the real data, how many tiers the page needs to show, or the connection and pool settings that kill the connection. Whether a plant should be listed as upstream of itself when a ring passes through it isn't stated either. The current query and the new function both list it.
