Decision: no-graph. Written up in docs/adr/0007-supplier-section-of-the-product-report.md.

Compliance need tier 1 only: the suppliers who deliver each item to us. That is one join from `supplies` to `party`
filtered on the buyer being us, which is what internal/queries/item_suppliers.sql already does; the sub-supplier rows
in the table are simply not reached. 600k rows, about 20 reports a day, 10 seconds allowed: nothing here traverses.
A graph database now would be built for a question nobody has asked. If compliance ever want deeper tiers, that is a
bounded walk on the same table first.
