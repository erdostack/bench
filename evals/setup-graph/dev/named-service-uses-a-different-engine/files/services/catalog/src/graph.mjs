import neo4j from "neo4j-driver";
import { requireEnv } from "@townmap/shared";

export const driver = neo4j.driver(
  process.env.TOWNMAP_GRAPH_URI ?? "bolt://localhost:7687",
  neo4j.auth.basic("neo4j", requireEnv("TOWNMAP_GRAPH_PASSWORD")),
);

export async function rows(query, params = {}) {
  const { records } = await driver.executeQuery(query, params, { routing: neo4j.routing.READ });
  return records.map((r) => r.toObject());
}
