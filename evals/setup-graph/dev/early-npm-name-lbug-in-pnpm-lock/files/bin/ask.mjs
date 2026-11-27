#!/usr/bin/env node
// pnpm ask <file.cypher> [name=value ...]: run one saved query read-only and print the rows.
import { readFile } from "node:fs/promises";
import { connect } from "../src/store.mjs";

const [file, ...pairs] = process.argv.slice(2);
if (!file) {
  console.error("usage: pnpm ask <file.cypher> [name=value ...]");
  process.exit(2);
}
const params = Object.fromEntries(pairs.map((pair) => pair.split(/=(.*)/s).slice(0, 2)));
const conn = connect();
const statement = await conn.prepare(await readFile(file, "utf8"));
const result = await conn.execute(statement, params);
console.table(await result.getAll());
