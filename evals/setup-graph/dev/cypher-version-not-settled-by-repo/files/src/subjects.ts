import { readFile } from "node:fs/promises";
import { read } from "./graph.js";

const saved = (name: string) => readFile(new URL(`../queries/${name}.cypher`, import.meta.url), "utf8");

/** The chain of broader subjects above a subject, nearest first. */
export async function broader(subject: string) {
  return read(await saved("broader_subjects"), { subject });
}

/** Works filed under a subject or anything narrower. */
export async function worksUnder(subject: string, limit = 50) {
  return read(await saved("works_under_subject"), { subject, limit });
}
