# Retention

Finance policy FP-12 (agreed with the external auditors, 2023):

- A purchase order is kept for ten years after its order date, with its lines, its supplier and the products
  on it, exactly as they were ordered. Auditors open orders from 2016 and expect to see the product's name
  and category.
- So nothing an order points at may be deleted while that order is kept. A product or supplier that we stop
  buying is **retired**: `retired_on` is set to the day it left the catalogue, and it stays in the graph.
- The buyer screens show only what can be bought today, so every statement in `catalogue.cypher` that lists
  products or suppliers filters on `retired_on IS NULL`. `product_page` is the exception on purpose (see the
  README). The audit statements never filter on it.
- The price paid is stored on the order line (`LINE.unit_price_cents`), because the catalogue price changes.

Orders older than ten years, and retired products no order points at any more, are removed by the
records team's yearly purge, which is run by hand from their own tooling and is not part of this repo.
