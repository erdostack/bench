# crumb

Orders and invoices for a wholesale bakery that supplies cafes, shops and canteens. The data lives in a
LadybugDB database file inside the office app (one process, one user at a time).

    db/schema.cypher    table definitions
    db/invoicing.cypher the statements the app runs for orders and invoices; each has a `// name:` line
    docs/invoicing.md   the rules invoices have to follow

About 420 customers, 160 products, 30,000 invoices since 2019 and 140,000 invoice lines.
