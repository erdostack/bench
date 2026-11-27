import { createServer } from "node:http";
import { log } from "@townmap/shared";
import { sameWard } from "./places.mjs";

createServer(async (req, res) => {
  const url = new URL(req.url, "http://localhost");
  const body = await sameWard(url.searchParams.get("id"), url.searchParams.get("kind") ?? "library");
  res.setHeader("content-type", "application/json");
  res.end(JSON.stringify(body));
}).listen(3001, () => log("catalog", "listening", { port: 3001 }));
