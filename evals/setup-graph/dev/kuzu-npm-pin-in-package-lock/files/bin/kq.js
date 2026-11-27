#!/usr/bin/env node
// npm run kq -- <file.cypher>
const fs = require("node:fs");
const { open } = require("../src/db");

(async () => {
  const file = process.argv[2];
  if (!file) {
    console.error("usage: npm run kq -- <file.cypher>");
    process.exit(2);
  }
  const { conn } = open({ readOnly: true });
  const result = await conn.query(fs.readFileSync(file, "utf8"));
  console.table(await result.getAll());
})();
