// name: add_product
MATCH (s:Supplier {code: $supplier})
WHERE s.retired_on IS NULL
CREATE (p:Product {sku: $sku, name: $name, category: $category,
                   unit_price_cents: $unit_price_cents, added_on: date()})
CREATE (s)-[:SUPPLIES]->(p);

// name: change_price
MATCH (p:Product {sku: $sku})
WHERE p.retired_on IS NULL
SET p.unit_price_cents = $unit_price_cents;

// name: retire_product
MATCH (p:Product {sku: $sku})
WHERE p.retired_on IS NULL
SET p.retired_on = date();

// name: retire_supplier
// also retires every product the supplier still has in the catalogue
MATCH (s:Supplier {code: $supplier})
WHERE s.retired_on IS NULL
SET s.retired_on = date()
WITH s
MATCH (s)-[:SUPPLIES]->(p:Product)
WHERE p.retired_on IS NULL
SET p.retired_on = date();

// name: import_orders
// nightly, one row per order line, rows arrive as $rows
UNWIND $rows AS row
MATCH (s:Supplier {code: row.supplier_code})
MATCH (p:Product {sku: row.sku})
MERGE (o:PurchaseOrder {number: row.po_number})
  ON CREATE SET o.placed_on = date(row.placed_on), o.placed_by = row.buyer
MERGE (o)-[:TO]->(s)
MERGE (o)-[l:LINE {line_no: toInteger(row.line_no)}]->(p)
SET l.qty = toInteger(row.qty),
    l.unit_price_cents = toInteger(row.unit_price_cents);
