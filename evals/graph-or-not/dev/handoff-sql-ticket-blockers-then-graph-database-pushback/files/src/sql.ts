import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

export function load(name: string): string {
  return readFileSync(fileURLToPath(new URL(`./panels/${name}`, import.meta.url)), "utf8");
}
