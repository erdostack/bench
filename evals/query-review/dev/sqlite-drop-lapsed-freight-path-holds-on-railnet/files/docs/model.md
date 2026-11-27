# Model

| node kind | code | |
|---|---|---|
| `path` | `P-6M42-WKD` | a timetable path (headcode, days it runs) |
| `holder` | `H-0042` | a freight operator or a customer holding capacity |
| `route` | `R-SEV-03` | a route section |

| edge kind | src | dst | |
|---|---|---|---|
| `holds` | holder | path | a hold on the path; `until` is its last day (`YYYY-MM-DD` text), NULL for an open-ended framework hold |
| `runs_over` | path | route | the route sections the path uses |

A path can be held by several holders on different days. Holds whose `until` is before the first day of
the current month have lapsed and are cleared before each month's allocation; open-ended holds never lapse.
The clearance run in November 2026, before the December 2026 allocation, removes the holds whose `until` is
before 2026-11-01.
