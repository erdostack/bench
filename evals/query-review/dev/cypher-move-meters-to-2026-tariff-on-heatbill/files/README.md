# heatbill

Billing graph for the district heating scheme: customer accounts, the heat meters in their properties, and
the tariff each meter is billed under (`docs/model.md`). The monthly bill run and the customer portal read it.

- `bin/hb <target> "<cypher>"` or `bin/hb <target> --file <file>` runs Cypher through cypher-shell
  (`config/targets.toml`). Every call is logged to `.hb_history` first.
- `changes/`: data changes, `YYYYMMDD-<what>.cypher`.
- `docs/ENVIRONMENTS.md`: read before changing anything.
