#!/usr/bin/env node
// Rebuilds the database file from data/*.csv. Destructive: removes the old file first.
const fs = require("node:fs");
const path = require("node:path");
const { open, DB_PATH } = require("../src/db");

(async () => {
  fs.rmSync(DB_PATH, { recursive: true, force: true });
  fs.mkdirSync(path.dirname(DB_PATH), { recursive: true });
  const { conn } = open({ readOnly: false });
  const ddl = fs.readFileSync(path.join(__dirname, "..", "db", "schema.cypher"), "utf8");
  for (const statement of ddl.split(";").map((s) => s.trim()).filter(Boolean)) {
    await conn.query(statement);
  }
  for (const table of ["Game", "Designer", "Mechanic", "DESIGNED", "HAS_MECHANIC"]) {
    await conn.query(`COPY ${table} FROM "data/${table.toLowerCase()}.csv" (header=true)`);
  }
})();
