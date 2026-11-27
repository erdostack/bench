# also_bought

One row per unordered pair of products, stored with the smaller product id in `a`:
`(a, b, orders)` with `a < b`. `orders` is how many orders contained both products; the importer adds
each day's count to the pair's row (inserting it the first time).

`recs/also_bought.py` looks a product up in both columns.
