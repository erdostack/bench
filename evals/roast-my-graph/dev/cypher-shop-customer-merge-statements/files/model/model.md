# Model

| Relationship | Meaning |
|---|---|
| `(:Customer)-[:PLACED]->(:Order)` | orders, kept forever for accounting |
| `(:Customer)-[:LIVES_AT {primary}]->(:Address)` | saved addresses |
| `(:Customer)-[:WROTE]->(:Review)-[:OF]->(:Product)` | product reviews, shown on the product page with the author's name |
| `(:Customer)-[:SUBSCRIBED_TO {since, next_delivery}]->(:Plan)` | paid recurring deliveries; billing reads this every night |
| `(:Customer)-[:REFERRED]->(:Customer)` | who brought whom; both directions occur between duplicates |

Constraints: `Customer.id`, `Order.number`, `Plan.code` unique.
