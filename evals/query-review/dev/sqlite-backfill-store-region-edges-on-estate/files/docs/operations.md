# Operations

## Targets

| Target | What it is |
|---|---|
| `estate` | The estate database itself. The store finder on the website, payroll's regional cost centres, the planogram tool and the region dashboards all read it. |
| `rehearsal` | `data/rehearsal.sqlite`, restored from `estate` every night. Rehearse changes here; nothing reads it. |

## Changes to estate

Data changes reach `estate` only as a file `changes/<YYYY-MM-DD>-<slug>.sql`, whose first line is
`-- why: <ticket and reason>`, reviewed in a PR and applied by the estate on-call with
`bin/apply estate changes/<file>.sql`. Rehearse it first with `bin/apply rehearsal changes/<file>.sql`.

`bin/apply` runs the file as one transaction and repeats it until a run changes no rows. Payroll reads
`edges` while it runs, so one run of a file may change at most 500 rows: a file that works in chunks
of up to 500 rows finishes on its own.
