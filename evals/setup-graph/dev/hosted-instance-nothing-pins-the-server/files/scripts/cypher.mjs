// npm run cypher -- <file.cypher>: one saved query, read session, rows as a table.
import { readFileSync } from "node:fs";
import { openDriver } from "../src/driver.mjs";

const file = process.argv[2];
if (!file) {
  console.error("usage: npm run cypher -- <file.cypher>");
  process.exit(2);
}
const driver = openDriver();
const session = driver.session({ defaultAccessMode: "READ" });
try {
  const result = await session.run(readFileSync(file, "utf8"));
  console.table(result.records.map((r) => r.toObject()));
} finally {
  await session.close();
  await driver.close();
}
