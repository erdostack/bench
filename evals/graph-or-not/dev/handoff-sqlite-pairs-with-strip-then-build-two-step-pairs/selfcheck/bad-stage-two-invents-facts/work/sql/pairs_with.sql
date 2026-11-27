SELECT product_b AS product_id FROM pairing WHERE product_a = :product_id
UNION
SELECT product_a FROM pairing WHERE product_b = :product_id;
