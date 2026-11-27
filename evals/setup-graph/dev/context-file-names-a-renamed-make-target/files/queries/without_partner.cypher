MATCH (t:Tree)-[:OF_VARIETY]->(v:Variety)
WHERE NOT EXISTS {
  MATCH (t)-[:IN_ROW]->(:Row)-[:ADJACENT_TO*0..2]-(:Row)<-[:IN_ROW]-(other:Tree)-[:OF_VARIETY]->(p:Variety)
  WHERE (v)-[:POLLINATED_BY]->(p)
}
RETURN t.tag AS tree, v.name AS variety
ORDER BY variety, tree;
