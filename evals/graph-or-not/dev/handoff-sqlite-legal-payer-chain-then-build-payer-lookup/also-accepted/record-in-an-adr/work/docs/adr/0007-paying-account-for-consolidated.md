# 0007. Paying account for consolidated invoicing

Status: Accepted
Date: 2026-11-23

Decision: recursive-sql

## Workload (stated by the billing team, 2026-11-23)

- The payer is the top of the account's legal chain: `account_link` rows with `kind = 'legal'`.
- `account.parent_account_id` is not used: 2022 CRM import, unmaintained, about a third wrong per sales.
- `kind = 'finance'` links are budget allocation and do not decide who is invoiced.
- 240k accounts, 61k legal links, longest legal chain 7.
- Monthly batch, 2 hour window, currently 9 minutes.

## Options

- graph-database: rejected. A second store for a monthly walk of at most 7 key lookups per account.
- in-process-library: workable (61k edges), but nothing is gained over one recursive query.
- recursive-sql: chosen.
- no-graph: rejected. Chains are of variable length.

## What would change this

- Invoicing becoming real-time per request, or chains getting much deeper.
