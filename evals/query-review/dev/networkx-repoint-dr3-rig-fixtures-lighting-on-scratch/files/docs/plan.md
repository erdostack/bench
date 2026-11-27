# The plan graph

Nodes have a `kind`: `fixture` (`F-0001` ...), `rack` (dimmer racks `DR-1` to `DR-6`), `universe`
(`U-1` to `U-4`), `distro` (power distribution `DISTRO-A`, `DISTRO-B`) and `splitter` (DMX splitters
`SPLIT-1`, `SPLIT-2`). Fixtures also carry `type` and `position` (`FOH`, `LX1` ... `LX4`, `BOOM-L`, `BOOM-R`).

| edge `kind` | from | to | attributes |
|---|---|---|---|
| `fed_by` | fixture | rack | `circuit` (1-48 on that rack) |
| `on_universe` | fixture | universe | `address` (DMX start address) |
| `powered_from` | rack | distro | `way` |
| `sends_data` | splitter | rack | |

Each rack has 48 circuits. DR-5 uses circuits 1-20; DR-3's fixtures are on circuits 21-48, so they keep
their circuit numbers if they move to DR-5.
