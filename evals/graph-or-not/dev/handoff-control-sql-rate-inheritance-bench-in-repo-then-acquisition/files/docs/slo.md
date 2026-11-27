# Service level objectives

| Endpoint | Objective |
|---|---|
| `GET /rates/effective` (booking engine, per room type) | p95 under 50 ms at the service, measured at the load balancer |
| `POST /rates` (revenue team) | p95 under 500 ms |

Revisit the storage design for a read path when it uses more than half its p95 objective in production.
