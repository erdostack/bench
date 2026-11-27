import { readFile } from "node:fs/promises";
import { read } from "./graph.js";

const saved = (name: string) => readFile(new URL(`../queries/${name}.cypher`, import.meta.url), "utf8");

export interface Usage {
  assembly: string;
  depth: number;
  quantity: number;
}

/** Every assembly that contains the part, directly or through sub-assemblies. */
export async function whereUsed(part: string): Promise<Usage[]> {
  return read<Usage>(await saved("where_used"), { part });
}

/** The flattened parts list of an assembly with multiplied-out quantities. */
export async function explode(assembly: string) {
  return read(await saved("exploded_bom"), { assembly });
}
