# Model

- `(:Bundle {sku, name, status, priceCents})`: status `draft`, `live` or `retired`; price in euro cents.
- `(:Bundle)-[:INCLUDES {qty}]->(:Product {sku})`
- `(:Collection {slug, title})`, unique on `slug` (constraint `collection_slug`).
- `(:Bundle)-[:IN_COLLECTION {addedAt}]->(:Collection)`: a bundle is in a collection at most once; the
  storefront lists a collection's bundles from these relationships.
