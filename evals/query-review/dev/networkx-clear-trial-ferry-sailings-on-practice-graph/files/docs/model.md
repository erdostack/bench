# Model

A `networkx.DiGraph`. Every node has a `kind`:

| kind | id | attributes |
|---|---|---|
| `port` | `PORT-BRAE` | `name` |
| `vessel` | `MV-SELVAY` | `name`, `cars` |
| `sailing` | `S-20261201-0710-BRAE` (timetabled), `EX-..`, `TRIAL-..` | `day` ('YYYY-MM-DD'), `departs` ('HH:MM') |

| edge `kind` | from | to |
|---|---|---|
| `departs` | sailing | port |
| `arrives` | sailing | port |
| `operated_by` | sailing | vessel |
| `connects_to` | sailing | sailing (a timed connection at the arrival port) |
