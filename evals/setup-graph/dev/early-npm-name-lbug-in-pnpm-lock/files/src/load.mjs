// node src/load.mjs <data dir>: rebuild var/wordroots.lbug from the CSV files.
import { mkdir, readFile, rm } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { connect, DB_PATH } from "./store.mjs";

const data = resolve(process.argv[2] ?? "data");
await rm(DB_PATH, { recursive: true, force: true });
await mkdir(dirname(DB_PATH), { recursive: true });

const conn = connect({ readOnly: false });
const ddl = await readFile(new URL("../schema/tables.cypher", import.meta.url), "utf8");
for (const statement of ddl.split(";").map((s) => s.trim()).filter(Boolean)) {
  await conn.query(statement);
}
await conn.query(`COPY Language FROM "${join(data, "languages.csv")}" (header=true)`);
await conn.query(`COPY Word FROM "${join(data, "words.csv")}" (header=true)`);
await conn.query(`COPY DERIVES_FROM FROM "${join(data, "derives.csv")}" (header=true)`);
console.log(`loaded ${data} into ${DB_PATH}`);
