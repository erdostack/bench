Added sql/controlled_companies.sql, returning (company_id, steps) with the fewest steps and leaving the client's
own company out. The walk carries the chain it came along, so rings in the holdings cannot loop it.

Decision to confirm: control is read as a stake of a quarter or more at every step, as docs/graph/DECISION.md
records. Other regimes use a majority instead:
- more than 50% at each step, or
- effective ownership, multiplying stakes along the chain (60% then 60% is 36%).
Tell me if compliance has moved to one of those and I will change the condition.

Checks:
- Tested on a small fixture: a direct 60% holding, a 30% holding one step further, a 10% holding left out and a
  two-company ring. The query returned the 60% and 30% companies at 1 and 2 steps.
