# Roast: staylist schema and queries

HotelAmenity is a reified edge; give it a better primary key.

## Findings

### 1. HotelAmenity (medium)

**Problem.** Intermediate node table (reified edge) adds a hop to amenity traversals.

**Fix.** Keep the table for flexibility but give it a composite primary key of hotel and amenity code to speed up lookups.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
