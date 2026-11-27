# Station model

Station `status`:

- `active`: reporting; has one `reports_to` edge to the hub that polls it.
- `retired`: stopped reporting on `retired_on`, still polled by its hub (`reports_to` kept) so late
  uploads from the logger are picked up.
- `archived`: a retired station we are done with: no `reports_to` edge, so the hub stops polling it.

Sensors keep their `installed_at` edge to the station whatever its status: it is the asset history.
