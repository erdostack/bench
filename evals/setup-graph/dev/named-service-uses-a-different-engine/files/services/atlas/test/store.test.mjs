import assert from "node:assert/strict";
import { test } from "node:test";
import { DB_PATH } from "../src/store.mjs";

test("the database file lives under the service's var directory", () => {
  assert.match(DB_PATH, /services\/atlas\/var\/paths\.lbug$/);
});
