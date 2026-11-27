# Model

| Pattern | Notes |
|---|---|
| `(:Rider {id, name, email, phone})` | |
| `(:Rider)-[:HAS_CARD]->(:PaymentCard {token, last4, expires})` | |
| `(:Rider)-[:TOOK]->(:Ride {id, startedAt, endedAt, distanceM, route})` | `route` is the GPS trace |
| `(:Ride)-[:FROM]->(:Dock)`, `(:Ride)-[:TO]->(:Dock {id, name, lat, lon})` | docks are public places |
| `(:Rider)-[:BILLED]->(:Invoice {number, issuedAt, net, vat, total, billingName, billingEmail, billingAddress})` | one per month with rides |
| `(:Invoice)-[:FOR]->(:Ride)` | the rides on the invoice |

Nothing else is attached to a rider.
