# Review

He's not right about Currency. 19 million relationships on EUR only hurt if a query walks out of EUR,
and none does: every query arrives at a currency from one payment and reads two properties. Nothing
deletes a currency, and per-currency totals happen in the warehouse. Keep the nodes; docs/model.md
gives a good reason for them. Nothing here needs changing before Black Friday.

## IN_CURRENCY (low)

Problem: Looks scary in a degree count (EUR has about 19 million), but every query arrives at the currency from a single payment and reads two properties. Nothing starts at a currency and walks out.

Fix: Keep it. Only worth revisiting if someone adds a query that starts from a currency.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
