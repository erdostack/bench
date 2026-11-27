// npm run seed: wipe the local database, apply db/constraints.cypher, load the course's sample shore.
import { graph } from "../src/graph.js";

const session = graph().session();
try {
  await session.run("MATCH (n) DETACH DELETE n");
  await session.run(`
    CREATE (splash:Zone {name: 'splash'}), (mid:Zone {name: 'mid shore'}), (low:Zone {name: 'low shore'})
    CREATE (algae:Species {name: 'sea lettuce', trophic_level: 1})-[:LIVES_IN]->(mid)
    CREATE (limpet:Species {name: 'limpet', trophic_level: 2})-[:LIVES_IN]->(mid)
    CREATE (winkle:Species {name: 'periwinkle', trophic_level: 2})-[:LIVES_IN]->(splash)
    CREATE (whelk:Species {name: 'dog whelk', trophic_level: 3})-[:LIVES_IN]->(mid)
    CREATE (star:Species {name: 'common starfish', trophic_level: 3})-[:LIVES_IN]->(low)
    CREATE (gull:Species {name: 'herring gull', trophic_level: 4})-[:LIVES_IN]->(splash)
    CREATE (limpet)-[:EATS]->(algae), (winkle)-[:EATS]->(algae), (whelk)-[:EATS]->(limpet),
           (star)-[:EATS]->(limpet), (gull)-[:EATS]->(star), (gull)-[:EATS]->(whelk), (gull)-[:EATS]->(winkle)`);
} finally {
  await session.close();
  await graph().close();
}
