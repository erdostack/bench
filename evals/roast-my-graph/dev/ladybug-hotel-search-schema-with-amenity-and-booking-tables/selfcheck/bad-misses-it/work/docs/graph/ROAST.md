# Roast: staylist schema and queries

Add an index for the city filter.

## Findings

### 1. hotels_with_amenities (medium)

**Problem.** Filters city with a scan of all hotels.

**Fix.** Add an index on Hotel.city.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
