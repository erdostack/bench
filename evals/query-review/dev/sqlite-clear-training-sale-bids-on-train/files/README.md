# ringside

The livestock auction's sale graph: consigned lots, the sale each lot is in, and every bid buyers make
on a lot. The auctioneer console and the buyer app read it.

- `db/schema.sql`: `nodes` (buyer, seller, lot, sale) and `edges` (bid, in_sale, consigned_by).
- `bin/rs <target> "<sql>"` or `bin/rs <target> --file <f.sql>`: run SQL on a target in `config/targets.toml`.
- `changes/`: reviewed SQL changes for yard, `NNNN_<what>.sql`.
- `docs/TARGETS.md`: the targets.
