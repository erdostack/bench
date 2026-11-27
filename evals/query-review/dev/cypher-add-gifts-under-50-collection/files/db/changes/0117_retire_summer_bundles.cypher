// GB-215: summer bundles are retired.
MATCH (b:Bundle) WHERE b.status = 'live' AND b.sku STARTS WITH 'SUM26-'
CALL (b) {
  SET b.status = 'retired'
} IN TRANSACTIONS OF 10000 ROWS;
