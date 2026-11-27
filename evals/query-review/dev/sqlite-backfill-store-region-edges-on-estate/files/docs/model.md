# Model

`nodes.kind`: `store` or `region`. Codes are unique (`ST-0412`, `R-NW`).

Store `status`: `planning` (a site we may open), `trading`, `refit` (temporarily shut for works, still
ours and still staffed) or `closed`. `region_code` is the region a store belongs to; it is kept on
closed and planned stores too, for history and for planning.

| edge kind | src | dst | columns |
|---|---|---|---|
| `in_region` | store | region | `since`: the store's `opened_on` |
| `manages` | region | store whose manager reports to the region (set by HR, not by us) | `since` |

Only stores we operate, `trading` or `refit`, have an `in_region` edge: the region dashboards and
payroll's regional cost centres count a region's stores by its `in_region` edges. A store's edge is
removed when it closes, and a planned site gets one when it opens.
