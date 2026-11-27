# Roast: supplymap (schema.sql, queries/, app/)

Verdict: The spinning page is `queries/upstream_tiers.sql`: a recursive query that cannot stop on a loop, and your data is made of loops. It is the only serious problem; the rest of the db layer is fine.

Judged against:
- Engine: PostgreSQL 16 (README.md), `postgres:16.4` in docker-compose.yml; the checks below ran on PostgreSQL 16.15.
- Size: about 14,000 companies and 90,000 supply links (README.md).
- Shape: suppliers often buy from their own customers and some groups trade in rings, so the graph has plenty of loops (README.md).
- Read: the risk page shows, for one plant, every company upstream, the lowest tier it appears at and one path; buyers open it many times a day (README.md).
- Write rate: not stated.

## Findings

### critical: `upstream_tiers.sql`
The query was told to follow suppliers upstream, and it will: round and round the resin maker and the packaging firm, forever, each lap a brand new row it is proud of.
Problem: The recursive CTE `upstream` carries `tier` and `path` and joins with `UNION`. UNION only drops rows that are identical in every column, and `tier` and `path` differ on every lap, so a loop is never recognised and the walk never stops. README.md says the graph has plenty of loops (suppliers that buy from their own customers, rings), and this is the risk page that buyers open many times a day. Run on PostgreSQL 16.15: a 4-company ring (1<-2<-3<-2, 4 supplies 3) hit a 5 s statement_timeout, and on 14,000 companies and 90,000 random links (the README's size) plant 1 hit a 20 s timeout. That is the page that spins until the connection is killed. Even without a loop the query enumerates every path rather than every company, which is exponential in the number of tiers.
Fix: Remove the cause: walk the graph breadth first and remember which companies were already reached, so each company is visited once, at its lowest tier. A recursive CTE cannot see rows from earlier laps, so do it in a function. Verified on PostgreSQL 16.15 with the 14,000/90,000 data (about 180 ms for 13,974 reachable companies, tiers identical to a reference walk, every path valid): `CREATE FUNCTION upstream_tiers(plant bigint) RETURNS TABLE (company_id bigint, name text, country char(2), tier int, path bigint[]) LANGUAGE plpgsql AS $$ DECLARE     t int := 1; BEGIN     DROP TABLE IF EXISTS pg_temp.seen;     CREATE TEMP TABLE seen (company_id bigint PRIMARY KEY, tier int NOT NULL, path bigint[] NOT NULL) ON COMMIT DROP;     INSERT INTO seen     SELECT DISTINCT ON (s.supplier_id) s.supplier_id, 1, ARRAY[s.customer_id, s.supplier_id]     FROM supplies s     WHERE s.customer_id = plant     ON CONFLICT DO NOTHING;     LOOP         INSERT INTO seen         SELECT DISTINCT ON (s.supplier_id) s.supplier_id, t + 1, f.path || s.supplier_id         FROM seen f         JOIN supplies s ON s.customer_id = f.company_id         WHERE f.tier = t         ON CONFLICT DO NOTHING;         EXIT WHEN NOT FOUND;         t := t + 1;     END LOOP;     RETURN QUERY     SELECT x.company_id, c.name, c.country, x.tier, x.path     FROM seen x JOIN company c ON c.id = x.company_id     ORDER BY x.company_id; END $$;` Then in app/risk_page.py replace the query text with `SELECT * FROM upstream_tiers(%(plant_id)s)` and delete queries/upstream_tiers.sql (or keep it as a comment of intent). Stopgap only, if the function cannot be deployed today: change `UNION` to `UNION ALL`, add `WHERE u.tier < 6` to the recursive step and `CYCLE company_id SET is_cycle USING cyc_path` after the CTE body, and filter `WHERE NOT is_cycle` in the final SELECT. That ran in 274 ms at tier cap 6 on the same data, but it still enumerates every simple path up to the cap and silently drops companies deeper than the cap.

### low: `upstream`
Problem: The function app/risk_page.py `upstream` sets no statement timeout, so a runaway query holds the page open until something else kills the connection, as reported, instead of failing fast with an error the page can show. This is not the cause of the spin (that is upstream_tiers.sql); it is why the symptom is a hang.
Fix: Inside the same transaction, before the query, run `cur.execute("SET LOCAL statement_timeout = '5s'")` (or set it on the page's database role with `ALTER ROLE <role> SET statement_timeout = '5s'`), and catch the resulting QueryCanceled to show an error.

## Holds up
- `supplies` primary key `(customer_id, supplier_id)`: leads with `customer_id`, which is what the upstream walk and `direct_suppliers.sql` filter on. No missing index here.
- `supplies_by_supplier`: leads with `supplier_id`, which `flagged_suppliers.sql` joins on (`s.supplier_id = f.company_id`); a primary key on `(customer_id, supplier_id)` cannot serve that, so the index is needed.
- `CHECK (supplier_id <> customer_id)`: removes one-company loops. Loops of two or more companies are real data (README.md) and remain; the check does not make the walk safe.
- The final `SELECT DISTINCT ON (u.company_id) ... ORDER BY u.company_id, u.tier` in `upstream_tiers.sql` does the right thing (lowest tier, one path per company); it is the recursive part above it that never finishes.
- `flagged_suppliers.sql` and `direct_suppliers.sql`: both join by primary key or by the indexes above, and neither recurses. `risk_flag` is keyed by `(company_id, reason)`, so a company is listed once per reason.

## Not checked
- The data is synthetic: random links at the README's size, since the real database is not in the repo. Real graphs are deeper or shallower than random ones, so the timings are indicative; the non-termination on any loop is not size dependent.
- The page code that calls `upstream` and the connection or pool settings that kill the connection are not in the repo.
- The maximum number of tiers the page needs to show is not stated.
- Whether the plant itself should be listed as upstream of itself when a ring passes through it is not stated, and the current query and the function above both list it.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
