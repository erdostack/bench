# Model

`nodes.kind` is `car`, `zone` or `depot`; `nodes.code` is unique (`CAR-FK-20417`, `Z-ORCHARD`, `D-NORTH`).
A car's `status` is `active` (bookable) or `retired` (sold or written off; kept for the trip history).

| edge kind | src | dst | rule |
|---|---|---|---|
| `based_in` | car | zone | the zone the car lives in; exactly one per car, retired cars keep their last one |
| `covered_by` | zone | depot | the depot whose crew looks after that zone; exactly one per zone |
| `serviced_by` | car | depot | the depot whose job list the car is on. Every **active** car has exactly one, to the depot that covers its zone. Retired cars have none: a retired car on a job list sends a crew to a car that is not there. |

Cars bought in the September 2026 batch went in through the fleet import, which wrote `based_in` and not
`serviced_by`, so those cars are on no depot's job list.
