// What: label past passengers whose last tour ended before 2024-01-01 as :Dormant, for Friday's mailing export.
// Only passengers who have travelled (lastTravelled is set); never-travelled enquirers must not be :Dormant (docs/mailing.md).
// Expected: about 71,000 passengers minus those already :Dormant.
// Count before/after (after should be 0):
// MATCH (p:Passenger) WHERE p.lastTravelled < date('2024-01-01') AND NOT p:Dormant RETURN count(p)
// Sanity check, should be 0 before and after:
// MATCH (p:Passenger:Dormant) WHERE p.lastTravelled IS NULL RETURN count(p)
MATCH (p:Passenger) WHERE p.lastTravelled < date('2024-01-01') AND NOT p:Dormant
CALL (p) { SET p:Dormant } IN TRANSACTIONS OF 10000 ROWS;
