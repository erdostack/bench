import { createServer } from "node:http";
import neo4j from "neo4j-driver";
import { firstPressing } from "./catalogue.js";

const driver = neo4j.driver(
  process.env.GRAPH_URI ?? "bolt://localhost:7687",
  neo4j.auth.basic("neo4j", process.env.GRAPH_PASSWORD ?? ""),
);

createServer(async (req, res) => {
  const catNo = new URL(req.url ?? "/", "http://localhost").searchParams.get("cat");
  const body = catNo ? await firstPressing(driver, catNo) : { error: "pass ?cat=<catalogue number>" };
  res.setHeader("content-type", "application/json");
  res.end(JSON.stringify(body));
}).listen(3000);
