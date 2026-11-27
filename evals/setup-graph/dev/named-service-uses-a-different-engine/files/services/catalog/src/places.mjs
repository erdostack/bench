import { rows } from "./graph.mjs";

const NEARBY = `
  MATCH (p:Place {id: $id})-[:IN_WARD]->(w:Ward)<-[:IN_WARD]-(other:Place)
  WHERE other <> p AND other.kind = $kind
  RETURN other.id AS id, other.name AS name
  ORDER BY name
  LIMIT 20`;

export const sameWard = (id, kind) => rows(NEARBY, { id, kind });
