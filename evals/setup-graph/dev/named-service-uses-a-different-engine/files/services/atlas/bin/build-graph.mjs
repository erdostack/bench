#!/usr/bin/env node
// Rebuilds var/paths.lbug from export/*.csv. Destructive; run by the print pipeline before each edition.
import { mkdirSync, readFileSync, rmSync } from "node:fs";
import { DB_PATH, open } from "../src/store.mjs";

rmSync(DB_PATH, { recursive: true, force: true });
mkdirSync(new URL("../var/", import.meta.url), { recursive: true });
const conn = open({ readOnly: false });
for (const statement of readFileSync(new URL("../schema/tables.cypher", import.meta.url), "utf8").split(";")) {
  if (statement.trim()) await conn.query(statement);
}
await conn.query('COPY Junction FROM "export/junctions.csv" (header=true)');
await conn.query('COPY PATH FROM "export/paths.csv" (header=true)');
