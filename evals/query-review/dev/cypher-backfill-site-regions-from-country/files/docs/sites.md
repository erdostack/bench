# Sites

`(:Site {code, name, country, region, regionSource})`, about 41,000 of them. `country` is the ISO 3166
alpha-2 code.

| Property | Meaning |
|---|---|
| `region` | monitoring region; drives which regional team plans the site's visits |
| `regionSource` | `'derived'` when `region` was computed from `country`; `'manual'` when the feasibility team set it by hand (border sites, sites in a multi-country network). A manual region is never overwritten by a change. Unset on sites that have never had a region. |

`(:Site)-[:RAN]->(:Study)`, `(:Site)-[:HAS]->(:Capability)`.

The visit planner reads sites all day: keep a transaction under 10,000 rows.
