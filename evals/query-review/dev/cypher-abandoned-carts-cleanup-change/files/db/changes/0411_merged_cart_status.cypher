// SHOP-1290: 4,100 guest carts merged before the status existed.
MATCH (g:Cart)-[:MERGED_INTO]->(:Cart)
WHERE g.status = 'open'
SET g.status = 'merged';
