// npm run cypher -- <file.cypher>: one saved query, read-only, rows as a table.
import { readFileSync } from "node:fs";
import { graph, read } from "../src/graph.js";

const file = process.argv[2];
if (!file) {
  console.error("usage: npm run cypher -- <file.cypher>");
  process.exit(2);
}
try {
  console.table(await read(readFileSync(file, "utf8")));
} finally {
  await graph().close();
}
