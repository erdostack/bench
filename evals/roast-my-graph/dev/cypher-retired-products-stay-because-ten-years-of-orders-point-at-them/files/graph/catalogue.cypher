// name: category_page
MATCH (s:Supplier)-[:SUPPLIES]->(p:Product)
WHERE p.category = $category AND p.retired_on IS NULL
RETURN p.sku AS sku, p.name AS name, p.unit_price_cents AS unit_price_cents, s.name AS supplier
ORDER BY p.name
LIMIT 100;

// name: supplier_catalogue
MATCH (s:Supplier {code: $supplier})-[:SUPPLIES]->(p:Product)
WHERE p.retired_on IS NULL
RETURN p.sku AS sku, p.name AS name, p.category AS category, p.unit_price_cents AS unit_price_cents
ORDER BY p.name;

// name: active_suppliers
MATCH (s:Supplier)
WHERE s.retired_on IS NULL
RETURN s.code AS code, s.name AS name
ORDER BY s.name;

// name: product_page
MATCH (s:Supplier)-[:SUPPLIES]->(p:Product {sku: $sku})
RETURN p.sku AS sku, p.name AS name, p.category AS category, p.unit_price_cents AS unit_price_cents,
       p.retired_on AS retired_on, s.code AS supplier_code, s.name AS supplier;
