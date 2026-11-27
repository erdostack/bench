# Model

- `Viewer {id}`
- `Title {id, name, synopsis, score, available}`; score is our 0 to 100 quality score
- `Genre {code, name}`

- `(:Viewer)-[:FAVOURS]->(:Genre)`
- `(:Viewer)-[:WATCHED {at, finished, position_s}]->(:Title)`
- `(:Title)-[:IN_GENRE]->(:Genre)`
