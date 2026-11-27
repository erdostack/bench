// Load data/campus.sqlite into an in-memory database inside the WebAssembly SQLite build.
import { readFileSync } from "node:fs";
import sqlite3InitModule from "@sqlite.org/sqlite-wasm";

export async function openCampus(file = process.env.WAYFIND_DB ?? "data/campus.sqlite") {
  const sqlite3 = await sqlite3InitModule({ print: () => {}, printErr: console.error });
  const bytes = readFileSync(file);
  const db = new sqlite3.oo1.DB();
  const p = sqlite3.wasm.allocFromTypedArray(bytes);
  const rc = sqlite3.capi.sqlite3_deserialize(db.pointer, "main", p, bytes.length, bytes.length,
    sqlite3.capi.SQLITE_DESERIALIZE_FREEONCLOSE);
  db.checkRc(rc);
  return { sqlite3, db };
}
