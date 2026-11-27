# Roast: parcelboard schema and queries

He's wrong about the tracking page. track starts from one shipment and takes one hop to its
carrier; customer_shipments starts from one customer. Neither ever walks the carrier's 14 million
shipments, so the size of Carrier does not matter to them, and there are no concurrent writers.
Only the monthly carrier_month batch reads a carrier's whole set, and it takes 25 seconds once a
month. No CarrierMonth bucketing needed. Details in docs/graph/ROAST.md and findings.json.

## Findings

### 1. carrier_month (medium)

**Problem.** The one statement that starts at a Carrier: it reads all of the carrier's shipments (14.2 million for the largest) to keep one month. It is a monthly batch of about 25 s, so it is not urgent.

**Fix.** If the batch window gets tight, keep a month column on SHIPPED_BY or load a per-month summary table; not needed before peak.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
