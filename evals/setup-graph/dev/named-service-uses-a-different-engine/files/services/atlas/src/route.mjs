import { open } from "./store.mjs";

// Fewest segments between two junctions, optionally avoiding steps.
export async function route(from, to, { stepFree = false } = {}) {
  const conn = open();
  const filter = stepFree ? "(r, n | WHERE NOT r.steps)" : "";
  const result = await conn.query(`
    MATCH p = (a:Junction {ref: '${from}'})-[:PATH* SHORTEST 1..60 ${filter}]-(b:Junction {ref: '${to}'})
    RETURN [n IN nodes(p) | n.ref] AS via, length(p) AS segments`);
  const rows = await result.getAll();
  return rows[0] ?? null;
}
