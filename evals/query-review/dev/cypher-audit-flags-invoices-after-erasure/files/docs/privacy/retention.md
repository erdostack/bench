# Retention and erasure

| Data | Kept | On erasure |
|---|---|---|
| Rider account (name, email, phone) | while the account is open | deleted |
| Payment cards | while the account is open | deleted |
| Rides, including GPS traces | 13 months | deleted |
| Invoices | **10 years from issue, required by tax law** | **kept, anonymised**: `billingName`, `billingEmail` and `billingAddress` are removed; number, date and amounts stay so the books still add up. The invoice is no longer linked to anyone once the rider and rides are gone. |
| Docks | always | not personal data, untouched |

The erasure script is `cypher/privacy/erase_rider.cypher`. Deleting invoices to complete an erasure is
not allowed: it breaks the tax retention duty, which takes precedence (Art. 17(3)(b) GDPR).
