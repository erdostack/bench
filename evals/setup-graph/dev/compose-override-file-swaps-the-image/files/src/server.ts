import { createServer } from "node:http";
import { dependants, stranded } from "./foodweb.js";
import { byZone } from "./zones.js";

createServer(async (req, res) => {
  const url = new URL(req.url ?? "/", "http://localhost");
  const name = url.searchParams.get("species") ?? "";
  const body =
    url.pathname === "/zones" ? await byZone() : url.pathname === "/stranded" ? await stranded(name) : await dependants(name);
  res.setHeader("content-type", "application/json");
  res.end(JSON.stringify(body));
}).listen(3000);
