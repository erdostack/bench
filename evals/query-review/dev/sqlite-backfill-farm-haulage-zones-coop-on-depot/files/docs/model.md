# Model

`nodes(id, kind, code, name, postcode, status)`: `kind` is `farm`, `store` (grain store) or `zone`
(haulage zone). `code` is unique: `F-004417`, `GS-ASH`, `HZ-03`. Farms have a `postcode` such as `LN4 2QT`.

`edges(id, kind, src, dst, since)`:

| kind | src | dst | notes |
|---|---|---|---|
| `member_of` | farm | store | the store a farm delivers to; `since` is a date |
| `in_zone` | farm | zone | the haulage zone a farm is collected in; no `since` (see `haulage.md`) |

`zone_districts(district, zone_code)`: which postcode district (`LN4`, `NG32`) each zone covers.
