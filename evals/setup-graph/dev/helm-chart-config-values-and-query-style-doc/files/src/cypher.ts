// yarn cypher <file.cypher> [--param key=value ...]: run one read query and print the records
import { readFileSync } from "node:fs";
import neo4j from "neo4j-driver";

const [file, ...rest] = process.argv.slice(2);
if (!file) throw new Error("usage: yarn cypher <file.cypher> [--param key=value ...]");
const params: Record<string, string> = {};
for (let i = 0; i < rest.length; i += 2) {
  if (rest[i] !== "--param") throw new Error(`unexpected argument ${rest[i]}`);
  const [k, ...v] = rest[i + 1].split("=");
  params[k] = v.join("=");
}
const driver = neo4j.driver(process.env.NEO4J_URI ?? "bolt://localhost:7687",
  neo4j.auth.basic(process.env.NEO4J_USER ?? "neo4j", process.env.NEO4J_PASSWORD ?? ""));
try {
  const { records } = await driver.executeQuery(readFileSync(file, "utf8"), params, { routing: neo4j.routing.READ });
  console.table(records.map((r) => r.toObject()));
} finally {
  await driver.close();
}
