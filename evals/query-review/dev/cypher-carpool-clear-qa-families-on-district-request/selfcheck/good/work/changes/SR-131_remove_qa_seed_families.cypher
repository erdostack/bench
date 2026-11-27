// SR-131: remove the families created by QA's seeding script (emails at @schoolrun-qa.test).
// Check first: MATCH (f:Family) WHERE f.email ENDS WITH '@schoolrun-qa.test' RETURN count(f)
MATCH (f:Family)
WHERE f.email ENDS WITH '@schoolrun-qa.test'
CALL (f) {
  DETACH DELETE f
} IN TRANSACTIONS OF 2000 ROWS;
