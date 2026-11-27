const path = require("node:path");
const kuzu = require("kuzu");

const DB_PATH = process.env.MEEPLE_DB || path.join(__dirname, "..", "var", "meeple.kz");

function open({ readOnly = true } = {}) {
  const db = new kuzu.Database(DB_PATH, 0, true, readOnly);
  return { db, conn: new kuzu.Connection(db) };
}

module.exports = { open, DB_PATH };
