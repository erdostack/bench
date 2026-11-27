// npm run seed: load data/ingredients.json and data/recipes.json into an empty database
import { readFileSync } from "node:fs";
import { connect } from "./graph.js";

const driver = connect();
const ingredients = JSON.parse(readFileSync("data/ingredients.json", "utf8"));
const recipes = JSON.parse(readFileSync("data/recipes.json", "utf8"));
await driver.executeQuery(readFileSync("schema/constraints.cypher", "utf8"));
await driver.executeQuery(
  `UNWIND $rows AS row MERGE (i:Ingredient {name: row.name})
   WITH i, row UNWIND row.subs AS s MERGE (j:Ingredient {name: s.name})
   MERGE (i)-[:SUBSTITUTES_FOR {ratio: s.ratio}]->(j)`, { rows: ingredients });
await driver.executeQuery(
  `UNWIND $rows AS row MERGE (r:Recipe {slug: row.slug})
   WITH r, row UNWIND row.uses AS u MATCH (i:Ingredient {name: u}) MERGE (r)-[:USES]->(i)`, { rows: recipes });
await driver.close();
