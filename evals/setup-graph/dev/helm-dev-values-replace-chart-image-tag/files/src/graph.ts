import neo4j, { type Driver } from "neo4j-driver";

let driver: Driver | undefined;

export function graph(): Driver {
  if (!driver) {
    const uri = process.env.PARTSBIN_GRAPH_URI ?? "bolt://localhost:7687";
    const user = process.env.PARTSBIN_GRAPH_USER ?? "neo4j";
    const password = process.env.PARTSBIN_GRAPH_PASSWORD;
    if (!password) throw new Error("PARTSBIN_GRAPH_PASSWORD is not set");
    driver = neo4j.driver(uri, neo4j.auth.basic(user, password));
  }
  return driver;
}

export async function read<T = Record<string, unknown>>(text: string, params: Record<string, unknown> = {}): Promise<T[]> {
  const result = await graph().executeQuery(text, params, { routing: neo4j.routing.READ });
  return result.records.map((record) => record.toObject() as T);
}
