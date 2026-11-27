# Review

The 'supernode' is harmless here; nothing traverses through it. No change needed.

## Currency (low)

Problem: High in-degree on EUR (19M IN_CURRENCY), but it is only ever an end point: queries go payment -> currency and nothing expands from a currency. No cost at query time.

Fix: Leave it. Revisit only if someone adds a query that starts at a currency.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
