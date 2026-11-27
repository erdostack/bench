#!/usr/bin/env node
// Rebuild db/survey.kuzu from schema.cypher and data/*.csv.
import { readFileSync, rmSync } from "node:fs";
import kuzu from "kuzu";

rmSync("db/survey.kuzu", { recursive: true, force: true });
const conn = new kuzu.Connection(new kuzu.Database("db/survey.kuzu"));
for (const statement of readFileSync("schema.cypher", "utf8").split(";")) {
  if (statement.trim()) await conn.query(statement);
}
await conn.query("COPY Species FROM 'data/species.csv' (header=true)");
await conn.query("COPY Site FROM 'data/sites.csv' (header=true)");
await conn.query("COPY SEEN_AT FROM 'data/sightings.csv' (header=true)");
