import neo4j from "neo4j-driver";

export function openDriver() {
  const { NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD } = process.env;
  if (!NEO4J_URI) {
    throw new Error("NEO4J_URI is not set: copy env.sample to .env and fill it in");
  }
  return neo4j.driver(NEO4J_URI, neo4j.auth.basic(NEO4J_USERNAME, NEO4J_PASSWORD));
}
