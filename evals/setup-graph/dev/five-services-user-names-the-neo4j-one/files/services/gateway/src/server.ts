import Fastify from "fastify";
import { routes } from "./routes.js";

const app = Fastify({ logger: true });
await app.register(routes);
await app.listen({ port: Number(process.env.PORT ?? 8080), host: "0.0.0.0" });
