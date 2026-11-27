# Model

| Relationship | From | To | Reads as |
|---|---|---|---|
| `RUNS_ON` | `Service` | `Host` | the service has an instance on the host |
| `DEPENDS_ON` | `Service` | `Service` | the first service calls the second |
| `OWNS` | `Team` | `Service` | the team is on call for the service |
| `MOUNTED_IN` | `Host` | `Rack` | physical hosts only |

Node keys: `Host.name`, `Service.name`, `Team.slug`, `Rack.code`.
Other properties: `Host.serial`, `Host.os`, `Service.tier` (1 to 4), `Team.pager`.
