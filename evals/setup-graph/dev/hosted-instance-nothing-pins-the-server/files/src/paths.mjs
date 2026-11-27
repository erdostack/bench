// Skills still missing on the way to a target skill, nearest first.
export const MISSING = `
  MATCH (target:Skill {slug: $target})-[:BUILDS_ON*1..6]->(needed:Skill)
  WHERE NOT EXISTS { (:Learner {id: $learner})-[:HAS]->(needed) }
  OPTIONAL MATCH (w:Workshop)-[:TEACHES]->(needed)
  RETURN needed.slug AS skill, collect(DISTINCT w.title) AS workshops`;

export async function missingSkills(driver, learner, target) {
  const { records } = await driver.executeQuery(MISSING, { learner, target }, { routing: "READ" });
  return records.map((r) => r.toObject());
}
