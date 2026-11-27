#!/usr/bin/env node
// npm run lq -w services/atlas -- <file.cypher>: run one saved query against the embedded file, read-only.
import { readFileSync } from "node:fs";
import { open } from "../src/store.mjs";

const file = process.argv[2];
if (!file) {
  console.error("usage: npm run lq -w services/atlas -- <file.cypher>");
  process.exit(2);
}
const result = await open().query(readFileSync(file, "utf8"));
console.table(await result.getAll());
