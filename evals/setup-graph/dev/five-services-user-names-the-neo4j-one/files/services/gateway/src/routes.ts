import type { FastifyInstance } from "fastify";

const upstream = {
  accounts: process.env.ACCOUNTS_URL ?? "http://localhost:8101",
  routing: process.env.ROUTING_URL ?? "http://localhost:8102",
  lineage: process.env.LINEAGE_URL ?? "http://localhost:8103",
};

export async function routes(app: FastifyInstance) {
  app.get("/healthz", async () => ({ ok: true }));
  for (const [name, base] of Object.entries(upstream)) {
    app.all(`/${name}/*`, async (request, reply) => {
      const target = base + request.url.slice(name.length + 1);
      const response = await fetch(target, { method: request.method, headers: { accept: "application/json" } });
      reply.code(response.status).send(await response.json());
    });
  }
}
