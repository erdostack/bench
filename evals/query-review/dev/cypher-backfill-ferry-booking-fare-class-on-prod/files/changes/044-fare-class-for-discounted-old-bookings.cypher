// 044: fare class for bookings made before 2026-03-01 that were sold at a discount, from the old
// discount table (export loaded as discounts-2026-03.csv: ref, fareClass). About 11,000 bookings.
// Count before and after: MATCH (b:Booking) WHERE b.fareClass IN ['concession', 'island-resident'] AND b.createdAt < datetime('2026-03-01T00:00:00Z') RETURN count(b);
// Reviewed by m.ross, run on prod 2026-03-02 by the duty ops engineer.
LOAD CSV WITH HEADERS FROM 'file:///discounts-2026-03.csv' AS row
MATCH (b:Booking {ref: row.ref})
CALL (b, row) {
  SET b.fareClass = row.fareClass
} IN TRANSACTIONS OF 10000 ROWS;
