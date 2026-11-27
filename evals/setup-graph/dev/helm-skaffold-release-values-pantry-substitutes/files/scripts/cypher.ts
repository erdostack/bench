// npm run cypher -- <file.cypher>: run one read query and print the records
import { readFileSync } from "node:fs";
import { connect } from "./graph.js";

const file = process.argv[2];
if (!file) throw new Error("usage: npm run cypher -- <file.cypher>");
const driver = connect();
try {
  const { records } = await driver.executeQuery(readFileSync(file, "utf8"), {},
    { routing: "READ" });
  console.table(records.map((r) => r.toObject()));
} finally {
  await driver.close();
}
