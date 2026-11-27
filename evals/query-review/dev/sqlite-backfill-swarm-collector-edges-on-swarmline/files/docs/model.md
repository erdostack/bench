# Model

`nodes.kind` is `report`, `member` or `area`; `nodes.code` is unique (`SR-2019-0412`, `M-0233`, `AR-07`).

For reports: `reported_on` is the day of the call (`YYYY-MM-DD`), `status` is `collected` (a member
collected the swarm), `unfounded` (someone went out and there was no honeybee swarm: wasps, bumblebees, a
swarm already gone) or `open`; `collector_code` is the member code of whoever went out, written by every
version of the app.

| edge kind | src | dst |
|---|---|---|
| `in_area` | report | the area it was in |
| `covers` | member | an area the member collects in |
| `collected_by` | report | the member who collected the swarm |

`collected_by` exists only for collected swarms: a report has one exactly when its status is `collected`
and its collector is a member in the register. The app has written it since the 2026 season; reports from
before then have the code but no edge. There are no foreign keys. Edge ids mean nothing outside the table.
