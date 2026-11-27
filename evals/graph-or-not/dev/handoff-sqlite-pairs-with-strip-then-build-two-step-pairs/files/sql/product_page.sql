-- Everything the product page header needs.
SELECT id, name, category, price_eur
FROM product
WHERE id = :product_id;
