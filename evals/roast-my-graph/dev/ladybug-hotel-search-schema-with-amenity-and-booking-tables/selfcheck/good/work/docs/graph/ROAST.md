# Roast: staylist schema and queries

One model change before the amenity filters: HotelAmenity is a node that only links a hotel to an
amenity, so make it an OFFERS relationship table from Hotel to Amenity with since and fee_eur. That
takes a hop out of every amenity search. Booking looks similar but reviews attach to it; keep it.
Details in docs/graph/ROAST.md and findings.json.

## Findings

### 1. HotelAmenity (medium)

**Problem.** A node table that only ever sits between one Hotel (OFFERS) and one Amenity (OF_AMENITY), holding since and fee_eur. Nothing else connects to it, so it is a relationship stored as a node: 1.3 million extra nodes and an extra hop in the amenity search that runs 400 times a second and is about to get more filters.

**Fix.** Replace it with CREATE REL TABLE OFFERS(FROM Hotel TO Amenity, since DATE, fee_eur DOUBLE) and match (h:Hotel)-[o:OFFERS]->(a:Amenity) in both queries.

### 2. Booking (low)

**Problem.** Also sits between a guest and a hotel, but a Review attaches to a specific booking and a guest books the same hotel many times. It is right as a node.

**Fix.** Keep it.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
