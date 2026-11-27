import { read } from "./graph.js";

// Everything that directly or indirectly feeds on a species: the animals that lose food if it disappears.
const DEPENDANTS = `
  MATCH (prey:Species {name: $name})<-[:EATS*1..6]-(predator:Species)
  RETURN DISTINCT predator.name AS species, predator.trophic_level AS level
  ORDER BY level, species`;

// Species that would be left with nothing to eat.
const STRANDED = `
  MATCH (gone:Species {name: $name})<-[:EATS]-(predator:Species)
  WHERE NOT EXISTS { (predator)-[:EATS]->(other:Species) WHERE other <> gone }
  RETURN predator.name AS species`;

export const dependants = (name: string) => read<{ species: string; level: number }>(DEPENDANTS, { name });
export const stranded = (name: string) => read<{ species: string }>(STRANDED, { name });
