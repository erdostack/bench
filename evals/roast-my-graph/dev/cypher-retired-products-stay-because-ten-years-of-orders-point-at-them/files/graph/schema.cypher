CREATE CONSTRAINT supplier_code IF NOT EXISTS FOR (s:Supplier) REQUIRE s.code IS UNIQUE;
CREATE CONSTRAINT product_sku IF NOT EXISTS FOR (p:Product) REQUIRE p.sku IS UNIQUE;
CREATE CONSTRAINT purchase_order_number IF NOT EXISTS FOR (o:PurchaseOrder) REQUIRE o.number IS UNIQUE;

CREATE INDEX product_category IF NOT EXISTS FOR (p:Product) ON (p.category);
