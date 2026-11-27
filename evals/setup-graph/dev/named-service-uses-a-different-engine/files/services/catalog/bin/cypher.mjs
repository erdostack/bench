#!/usr/bin/env node
// npm run cypher -w services/catalog -- <file.cypher>
import { readFileSync } from "node:fs";
import { driver, rows } from "../src/graph.mjs";

try {
  console.table(await rows(readFileSync(process.argv[2], "utf8")));
} finally {
  await driver.close();
}
