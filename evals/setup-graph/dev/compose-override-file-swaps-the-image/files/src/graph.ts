import neo4j, { type Driver } from "neo4j-driver";

let driver: Driver | undefined;

export function graph(): Driver {
  driver ??= neo4j.driver(
    process.env.TIDEPOOL_GRAPH_URI ?? "bolt://localhost:7687",
    neo4j.auth.basic("neo4j", process.env.TIDEPOOL_GRAPH_PASSWORD ?? ""),
  );
  return driver;
}

export async function read<T = Record<string, unknown>>(query: string, params: Record<string, unknown> = {}) {
  const { records } = await graph().executeQuery(query, params, { routing: neo4j.routing.READ });
  return records.map((r) => r.toObject() as T);
}
