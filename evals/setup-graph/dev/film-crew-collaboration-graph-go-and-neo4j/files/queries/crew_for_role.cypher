MATCH (p:Production {id: $production})
CALL (p) {
  MATCH (p)<-[c:CREDITED_ON]-(person:Person)
  RETURN c.role AS role, collect(person.name) AS people
}
RETURN role, people ORDER BY role;
