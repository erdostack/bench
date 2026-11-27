// npm run cq -- <file.cypher> [name=value ...]: run one saved query read-only and print the rows.
import { readFile } from "node:fs/promises";
import { close, read } from "../src/graph.js";

const [file, ...pairs] = process.argv.slice(2);
if (!file) {
  console.error("usage: npm run cq -- <file.cypher> [name=value ...]");
  process.exit(2);
}
const params = Object.fromEntries(pairs.map((pair) => {
  const at = pair.indexOf("=");
  return [pair.slice(0, at), pair.slice(at + 1)];
}));
console.table(await read(await readFile(file, "utf8"), params));
await close();
