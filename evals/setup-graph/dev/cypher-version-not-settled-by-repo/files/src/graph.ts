import neo4j, { type Driver } from "neo4j-driver";

let driver: Driver | undefined;

function connect(): Driver {
  const password = process.env.STACKS_GRAPH_PASSWORD;
  if (!password) throw new Error("STACKS_GRAPH_PASSWORD is not set");
  return neo4j.driver(process.env.STACKS_GRAPH_URI ?? "bolt://localhost:7687", neo4j.auth.basic("neo4j", password));
}

export async function read(text: string, params: Record<string, unknown> = {}) {
  driver ??= connect();
  const { records } = await driver.executeQuery(text, params, { routing: neo4j.routing.READ });
  return records.map((record) => record.toObject());
}

export async function close() {
  await driver?.close();
  driver = undefined;
}
