// name: purge_closed_merchants
MATCH (m:Merchant)
WHERE m.closed_on < date() - duration({years: 7})
CALL (m) {
  DETACH DELETE m
} IN TRANSACTIONS OF 10000 ROWS;

// name: purge_expired_coupons
MATCH (c:Coupon)
WHERE c.expires_on < date() - duration({years: 1})
CALL (c) {
  DETACH DELETE c
} IN TRANSACTIONS OF 10000 ROWS;
