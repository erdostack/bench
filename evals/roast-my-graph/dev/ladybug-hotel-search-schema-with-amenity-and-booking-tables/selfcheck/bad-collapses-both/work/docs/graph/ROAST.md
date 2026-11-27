# Roast: staylist schema and queries

Two join nodes to flatten: HotelAmenity and Booking.

## Findings

### 1. HotelAmenity (medium)

**Problem.** Join node; should be a relationship.

**Fix.** Make it a rel table.

### 2. Booking (high)

**Problem.** Also a join node between Guest and Hotel; adds a hop to every account query.

**Fix.** Replace with a STAYED_AT relationship from Guest to Hotel carrying check_in and nights.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
