# Data notes

- Junction ids are `J-` plus four digits, assigned by the GIS team.
- `segment.km` is the surveyed length; `surface` is one of paved, gravel, dirt, scramble.
- Closures: `make close` deletes the junction. The schema's cascade deletes the segments that touch it, so
  nothing else has to be cleaned up.
