# Model

- `(:Customer {customerId})-[:HAS_CART]->(:Cart {cartId, status, createdAt, updatedAt})`
- `(:Cart)-[:CONTAINS {qty, addedAt}]->(:Product {sku})`
- `(:Order {orderId})-[:FROM_CART]->(:Cart)` for carts that became orders

`Cart.status` is `open`, `ordered` or `merged` (a guest cart merged into a customer's cart on
login). `updatedAt` is a DATETIME, set on every change to the cart. Counts (2026-11-20): 31 million
carts, of which about 14 million are open and not updated since before 2026-08-25; 3.4 items per
cart on average.
