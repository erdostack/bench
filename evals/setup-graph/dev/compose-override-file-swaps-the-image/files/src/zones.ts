import { read } from "./graph.js";

const BY_ZONE = `
  MATCH (z:Zone)<-[:LIVES_IN]-(s:Species)
  RETURN z.name AS zone, count(s) AS species, avg(s.trophic_level) AS mean_level
  ORDER BY zone`;

export const byZone = () => read<{ zone: string; species: number; mean_level: number }>(BY_ZONE);
