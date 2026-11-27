// Opening the embedded database. Everything else imports connect() from here.
import { Connection, Database } from "lbug";
import { fileURLToPath } from "node:url";

export const DB_PATH = process.env.WORDROOTS_DB ?? fileURLToPath(new URL("../var/wordroots.lbug", import.meta.url));

export function connect({ readOnly = true } = {}) {
  const database = new Database(DB_PATH, 0, true, readOnly);
  return new Connection(database);
}
