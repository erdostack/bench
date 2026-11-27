# Roast: parcelboard schema and queries

Nothing has to change. The tracking and portal queries arrive at Carrier from a single shipment,
they never fan out from it, so 14 million relationships on one carrier cost them nothing extra.
Skip the bucketing.

## Findings

Nothing to report.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
