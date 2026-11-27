# Model

A `networkx.DiGraph`, saved with `networkx.node_link_data(G)`.

Nodes, keyed by code, with a `kind` attribute:

- `club` (`CL-0112`): `name`, `founded` (a year).
- `team` (`TM-04410`): `name`, `age_group`.
- `ground` (`GR-031`): `name`.

Edges, with a `kind` attribute:

| kind | from | to | attributes |
|---|---|---|---|
| `of_club` | team | club | |
| `home_ground` | club | ground | `since` (a year) |
| `affiliated_to` | club | club | the club is a satellite of the other |
