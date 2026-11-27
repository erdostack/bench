import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { test } from "node:test";

const rows = async (name) => (await readFile(new URL(`../data/${name}`, import.meta.url), "utf8")).trim().split("\n").slice(1);

test("every derivation points at words that exist", async () => {
  const ids = new Set((await rows("words.csv")).map((line) => line.split(",")[0]));
  for (const line of await rows("derives.csv")) {
    const [from, to, kind] = line.split(",");
    assert.ok(ids.has(from) && ids.has(to), line);
    assert.ok(["borrowed", "inherited", "derived", "calque"].includes(kind), line);
  }
});
