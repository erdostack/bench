# Roast: nookbook model

A foreign key in a property, in a graph database. We meet again.

## Findings

### 1. Listing.city_slug (critical)

**Problem.** Denormalised foreign key stored as a property alongside the IN relationship. Two sources of truth violate the single-source-of-truth principle and will drift; this is the relational habit graph modelling exists to remove.

**Fix.** Drop city_slug and the listing_city_price index. Rewrite search_city to anchor on (c:City {slug: $city})<-[:IN]-(l:Listing) and filter on price.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
