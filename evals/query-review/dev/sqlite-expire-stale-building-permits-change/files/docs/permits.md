# Permits

## Status

`open` (issued, work under way), `finaled` (final inspection passed), `expired`, `revoked`.

## Lapse rule (building code s. 105.5, as the city applies it)

An open permit lapses when 18 months pass with no inspection. The 18 months run from the later of the
issue date and the most recent inspection, so a permit issued last month with no inspection yet has not
lapsed.

A permit whose holder has an open appeal is on hold and does not lapse, however old it is. Appeals are
`appeal` nodes with an `APPEALS` edge to the permit; status `open` until the board decides, then `upheld`
or `dismissed`. Only open appeals hold a permit.

## Graph

| kind | columns used |
|---|---|
| `permit` | `ref` (BP-yyyy-nnnnn), `status`, `issued_on` |
| `inspection` | `ref`, `done_on` |
| `appeal` | `ref`, `status` |
| `parcel` | `ref` (APN) |

| rel | from | to |
|---|---|---|
| `ON` | permit | parcel |
| `INSPECTS` | inspection | permit |
| `APPEALS` | appeal | permit |
