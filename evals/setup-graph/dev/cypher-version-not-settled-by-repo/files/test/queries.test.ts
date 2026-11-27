import assert from "node:assert/strict";
import { readdir, readFile } from "node:fs/promises";
import { test } from "node:test";

test("saved queries only read and bound their variable-length patterns", async () => {
  for (const name of await readdir("queries")) {
    const text = await readFile(`queries/${name}`, "utf8");
    assert.ok(!/\b(CREATE|MERGE|DELETE|SET|REMOVE)\b/i.test(text), `${name} writes`);
    assert.ok(!/\*\s*\]/.test(text), `${name} has an unbounded pattern`);
  }
});
