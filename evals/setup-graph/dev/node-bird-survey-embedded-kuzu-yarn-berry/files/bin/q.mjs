#!/usr/bin/env node
// node bin/q.mjs <file.cypher>: run one saved query against db/survey.kuzu, read-only.
import { readFileSync } from "node:fs";
import kuzu from "kuzu";

const db = new kuzu.Database("db/survey.kuzu", 0, true, true);
const conn = new kuzu.Connection(db);
const result = await conn.query(readFileSync(process.argv[2], "utf8"));
for (const row of await result.getAll()) console.log(JSON.stringify(row));
