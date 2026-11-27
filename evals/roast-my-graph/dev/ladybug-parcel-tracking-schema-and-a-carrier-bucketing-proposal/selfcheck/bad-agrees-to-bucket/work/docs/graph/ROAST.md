# Roast: parcelboard schema and queries

The reviewer is right: bucket Carrier into CarrierMonth before peak season.

## Findings

### 1. Carrier (critical)

**Problem.** Supernode with 14.2M SHIPPED_BY relationships; every query that touches it slows down.

**Fix.** Introduce CarrierMonth nodes and link shipments to the month bucket.

### 2. track (high)

**Problem.** Touches the Carrier supernode on every request.

**Fix.** Use the buckets.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
