import type { Driver } from "neo4j-driver";

// Follow REISSUE_OF back to the first pressing. Bounded: no real chain in the shop is longer than a dozen.
const ORIGIN = `
  MATCH (p:Pressing {catalogue_no: $catNo})-[:REISSUE_OF*0..12]->(first:Pressing)
  WHERE NOT (first)-[:REISSUE_OF]->()
  MATCH (first)-[:ON_LABEL]->(l:Label)
  RETURN first.catalogue_no AS catalogueNo, first.year AS year, l.name AS label`;

export async function firstPressing(driver: Driver, catNo: string) {
  const { records } = await driver.executeQuery(ORIGIN, { catNo }, { routing: "READ" });
  return records[0]?.toObject() ?? null;
}
