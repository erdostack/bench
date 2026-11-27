MATCH (:Customer {customerId: $customerId})-[:HAS_CART]->(c:Cart {status: 'open'})
OPTIONAL MATCH (c)-[i:CONTAINS]->(p:Product)
RETURN c.cartId AS cartId, collect({sku: p.sku, qty: i.qty}) AS items;
