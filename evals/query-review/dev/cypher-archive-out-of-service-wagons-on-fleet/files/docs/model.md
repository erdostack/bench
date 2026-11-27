# Model (Neo4j 5.26)

    (:Wagon {wagonNo, type, status})-[:KEPT_BY]->(:Keeper)
    (:Wagon)-[:MAINTAINED_AT]->(:Depot)
    (:Wagon)-[:ALLOCATED_TO]->(:Flow)

`Wagon.status` is one of:

| status | meaning |
|---|---|
| `active` | in traffic |
| `workshop` | in a depot for repair or a periodic exam; back in traffic within weeks |
| `stored` | parked out of traffic in a siding (seasonal or mothballed); returns when demand comes back |
| `scrapped` | cut up; will never run again |
| `sold` | sold out of the fleet to another keeper |

A wagon that has left the fleet (`scrapped` or `sold`) is archived: it carries the label `ArchivedWagon`
instead of `Wagon`, keeps its properties and relationships, and drops out of every screen. Wagons in the
workshop or in store are still fleet and keep the `Wagon` label; the maintenance planner and the
seasonal-demand plan need them.

Counts (2026-11-20): 31,400 wagons: 24,950 active, 1,240 workshop, 2,310 stored, 2,180 scrapped, 720 sold.
