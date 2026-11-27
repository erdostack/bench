# Targets

| Target | What it is |
|---|---|
| `crewlink` | The rounds graph. The CrewLink in-cab app the crews use, the contact centre's screens and the council website's bin-day lookup all run on it. Named after the app, which came first. |
| `rehearse` | Restored from last night's `crewlink` backup. Nothing reads it; try anything here. |

## Changing crewlink

A data change on `crewlink` is a file `changes/NNNN_<what>.cypher` (next free number) whose first line is a
comment giving the ticket and what it does. It is reviewed in a PR and the rounds on-call runs it with
`bin/cl crewlink --file changes/<file>`. Nobody writes to `crewlink` any other way.

The in-cab app writes collections into `crewlink` all day and gives up on a write after five seconds, so a
change commits at most 10,000 rows per transaction.
