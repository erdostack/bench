import assert from "node:assert/strict";
import { readdirSync, readFileSync } from "node:fs";
import { test } from "node:test";

for (const name of readdirSync(new URL("../cypher/", import.meta.url))) {
  test(`${name} is bounded and returns rows`, () => {
    const text = readFileSync(new URL(`../cypher/${name}`, import.meta.url), "utf8");
    assert.match(text, /RETURN/);
    assert.doesNotMatch(text, /\*\]/);
  });
}
