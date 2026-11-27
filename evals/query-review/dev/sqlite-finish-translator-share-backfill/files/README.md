# royalties

Who earns on which book, for Calder & Finch's royalty run. `nodes` holds contributors and titles;
`edges` holds `earns_on` (contributor -> title) with the contributor's role and share in basis points.

- `contract_import`: contracts loaded from the rights system's export, one row per signed contract.
- `jobs/`: one module per job, `python3 -m jobs <job>`, each with `run(conn)`.
- `docs/royalties.md`: how shares are modelled. `docs/jobs.md`: how jobs are scheduled.
