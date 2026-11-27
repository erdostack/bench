# buyline

The purchasing catalogue of a hospital group: suppliers, the products they supply, and the purchase orders
placed with them. Neo4j 5.26. The buyer screens read the catalogue; finance and the external auditors read
the orders.

    graph/schema.cypher      constraints and indexes
    graph/writes.cypher      catalogue changes made from the buyer screens, and the nightly order import
    graph/catalogue.cypher   what the buyer screens run; each statement has a `// name:` line
    graph/audit.cypher       what finance and the auditors run
    docs/retention.md        what we must keep, and for how long

## Numbers

| Thing | Count |
|---|---|
| `Supplier` | 1,900 (about 1,150 active) |
| `Product` | 64,000 (about 18,000 active) |
| `PurchaseOrder` | 210,000, about 21,000 a year |
| `LINE` | 1.3 million |

`category_page` and `supplier_catalogue` are the busy ones, a few calls a second during office hours.
`product_page` is opened from search results and from the lines of old orders, so it also shows retired
products (the screen puts a "retired" banner on them). The audit statements run a few times a month.

## Import

Orders are raised in the ERP and imported every night by `import_orders`, one row per order line. The ERP
sends an order once, when it is approved, and an approved order is never changed (a correction is a new
order). Products are created in this catalogue first and the ERP copies them, so every SKU in the import
already exists here. Dates arrive as ISO text (`2026-03-14`); the audit tool passes `$from` and `$to` as
dates.
