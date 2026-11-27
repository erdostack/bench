// People who shared at least two productions with $person, most shared first.
MATCH (me:Person {id: $person})
CALL {
  WITH me
  MATCH (me)-[:CREDITED_ON]->(prod:Production)<-[:CREDITED_ON]-(other:Person)
  WHERE other <> me
  RETURN other, count(DISTINCT prod) AS shared
}
WITH other, shared WHERE shared >= 2
RETURN other.id, other.name, shared
ORDER BY shared DESC, other.name;
