# shelfnote

Tablets on the shop floor of each store, for staff and customers. The app embeds LadybugDB; the
database file is rebuilt every night from the merchandising exports and opened read-only by the tablets'
API.

    schema/schema.cypher     node and relationship tables
    queries/tablet.cypher    every query the tablet API runs

## Sizes

| Table | Rows |
|---|---|
| Store | 1,400 (600 more next quarter) |
| Product | 26,000 |
| Promo | about 700 kept, 60 to 90 active at any time |
| RUNS_AT | each promotion runs in 20 to 200 stores (they are regional) |
| STOCKS | 9.8 million |
| NEAR | each store has its 10 nearest stores |

## Screens

- "Promotions in this store": `store_promos`, refreshed every five minutes; customers read it.
- "Promotion items": `promo_items` when someone taps a promotion.
- "Low stock": `low_stock`, staff only.
- "Transfer from another store": `transfer_distance`, staff only, a few times a day.
