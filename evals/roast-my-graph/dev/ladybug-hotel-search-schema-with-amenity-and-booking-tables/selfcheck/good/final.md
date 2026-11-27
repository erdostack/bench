One model change before the amenity filters: HotelAmenity is a node that only links a hotel to an
amenity, so make it an OFFERS relationship table from Hotel to Amenity with since and fee_eur. That
takes a hop out of every amenity search. Booking looks similar but reviews attach to it; keep it.
Details in docs/graph/ROAST.md and findings.json.
