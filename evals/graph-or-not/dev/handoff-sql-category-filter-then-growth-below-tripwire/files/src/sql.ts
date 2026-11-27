import { readFileSync } from "node:fs";
import { join } from "node:path";

const dir = join(import.meta.dirname, "..", "sql");
export const sql = (name: string): string => readFileSync(join(dir, `${name}.sql`), "utf8");
