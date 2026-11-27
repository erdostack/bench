// pnpm cypher <file.cypher>: run one read query and print the records
import { readFileSync } from "node:fs";
import { connect } from "./graph.mjs";

const file = process.argv[2];
if (!file) {
  console.error("usage: pnpm cypher <file.cypher>");
  process.exit(2);
}
const driver = connect();
try {
  const { records } = await driver.executeQuery(readFileSync(file, "utf8"), {}, { routing: "READ" });
  console.table(records.map((r) => r.toObject()));
} finally {
  await driver.close();
}
