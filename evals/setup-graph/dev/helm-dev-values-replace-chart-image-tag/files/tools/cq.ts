// npm run cq -- <file.cypher> [name=value ...]
// Runs one saved query in a read transaction and prints the rows as a table.
import { readFile } from "node:fs/promises";
import { graph, read } from "../src/graph.js";

const [file, ...pairs] = process.argv.slice(2);
if (!file) {
  console.error("usage: npm run cq -- <file.cypher> [name=value ...]");
  process.exit(2);
}
const params = Object.fromEntries(pairs.map((pair) => pair.split("=", 2) as [string, string]));
console.table(await read(await readFile(file, "utf8"), params));
await graph().close();
