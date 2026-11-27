# nookbook

Short-stay rentals. The catalogue graph is Neo4j 5.

    model/schema.cypher    constraints and indexes
    model/writes.cypher    the write statements the listing service runs
    model/reads.cypher     the read queries; each has a `// name:` line

## Workload

- `search_city` is the landing page of every city: listings in that city inside a price band, cheapest first,
  24 to a page. Around 1,800 calls a second at peak, budget 50 ms.
- `listing_page` and `host_listings` are the listing and host pages.
- `city_summary` runs once a night per city for the pricing report.

## Notes on the model

- A listing belongs to exactly one city and never changes city: a change of address is handled as a new
  listing. `create_listing` is the only statement that creates a listing.
- `Listing.city_slug` repeats the slug of the city the listing is `IN`. It was added in March so that
  `search_city` can be answered from the `listing_city_price` index. Before that the query went through the
  `City` node and sorted every listing in the city; p95 for the big cities was about 900 ms. It is 11 ms now.

## Size

| Thing | Count |
|---|---|
| `Listing` | 3.1 million |
| `City` | 9,400; the largest has 212,000 listings |
| `Host` | 1.2 million |
| `Amenity` | 85 |
