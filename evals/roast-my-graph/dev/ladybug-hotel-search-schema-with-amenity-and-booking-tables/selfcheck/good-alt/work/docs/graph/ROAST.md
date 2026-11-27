# Roast: staylist schema and queries

Turn HotelAmenity into a Hotel-to-Amenity rel table with its two properties.

## Findings

### 1. OFFERS / OF_AMENITY via HotelAmenity (high)

**Problem.** Two-hop link through an intermediate node table with no other edges; the search pays for it on every request.

**Fix.** One rel table Hotel->Amenity carrying since and fee_eur; drop HotelAmenity.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
