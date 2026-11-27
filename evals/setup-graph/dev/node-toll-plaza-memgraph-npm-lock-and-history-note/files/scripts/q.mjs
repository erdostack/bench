#!/usr/bin/env node
// node scripts/q.mjs <file.cypher> [name=value ...]: run one saved query in a read session.
import { readFileSync } from "node:fs";
import neo4j from "neo4j-driver";

const [file, ...pairs] = process.argv.slice(2);
const params = Object.fromEntries(pairs.map((pair) => {
  const at = pair.indexOf("=");
  return [pair.slice(0, at), pair.slice(at + 1)];
}));
const [user, password] = (process.env.NEO4J_AUTH ?? "/").split("/");
const driver = neo4j.driver(process.env.NEO4J_URI ?? "bolt://localhost:7687", neo4j.auth.basic(user, password ?? ""));
const session = driver.session({ defaultAccessMode: neo4j.session.READ });
try {
  const result = await session.run(readFileSync(file, "utf8"), params);
  for (const record of result.records) console.log(JSON.stringify(record.toObject()));
} finally {
  await session.close();
  await driver.close();
}
