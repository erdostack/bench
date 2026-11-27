Decision: recursive-sql

Finance's payer rule needs the whole chain above each organisation, which is a walk, but the chain is at most 6 levels deep and the org tree already sits in the SQLite file billing runs. A recursive query on that file is enough. A graph database is not needed.

The numbers: 14,000 organisations, at most 6 levels, so the monthly run reads at most 84,000 chain rows and the tooltip about 600 rows a day. In a synthetic run (14,000 generated organisations, 412 dangling parent_ids, not your data), a recursive query matched a Python walk that stops at the last existing organisation for every organisation, with no mismatches. The full pass took about 0.29 s.

The query (replace :x with the organisation id):

WITH RECURSIVE chain(id, parent_id, billing_account_id, depth) AS (
  SELECT id, parent_id, billing_account_id, 0 FROM org WHERE id = :x
  UNION ALL
  SELECT o.id, o.parent_id, o.billing_account_id, c.depth + 1
  FROM org o JOIN chain c ON o.id = c.parent_id
  WHERE c.depth < 32)
SELECT COALESCE((SELECT id FROM chain WHERE billing_account_id IS NOT NULL
                 ORDER BY depth DESC LIMIT 1), :x);

It picks the highest organisation with an account, so it has to read the whole chain rather than stop at the first account it meets. The walk ends at a missing parent, so the 412 orphaned chains end at the last existing organisation, as Finance asked. The depth cap of 32 is only a guard against a parent cycle; Finance's limit is 6. Whether the live data has cycles is unknown to me.

Not done: I did not change billing/invoices.py or the schema. The real billing file (var/billing.db) is not in the repo, so the real chain depths and account counts are unknown.

What would change this: chains deeper than 6 in the live data, or the lookup running many times a second, measured on the real file. Either would make in-process-library the next option to test. Tomasz's graph database would need a requirement beyond parent-chain lookups, such as ownership across branches.

Full write-up: /run/work/docs/graph/DECISION.md
