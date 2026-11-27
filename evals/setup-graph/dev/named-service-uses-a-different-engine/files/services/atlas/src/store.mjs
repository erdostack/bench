// The embedded path-network database. Read-only unless the builder opens it.
import lbug from "@ladybugdb/core";

export const DB_PATH = new URL("../var/paths.lbug", import.meta.url).pathname;

export function open({ readOnly = true } = {}) {
  const db = new lbug.Database(DB_PATH, 0, true, readOnly);
  return new lbug.Connection(db);
}
