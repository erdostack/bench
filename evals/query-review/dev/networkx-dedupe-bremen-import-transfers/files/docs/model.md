# Model

- Edge key: the transfer id (`T` + number). Attributes: `object` (accession number), `year`, `method`
  (sale, gift, bequest, exchange, consignment, restitution), `batch` (the import it came from).
- Many edges can join the same two parties. A dealer sells dozens of sheets to the same collector, and
  the same sheet can pass between the same two parties more than once (consigned in 1921 and sold to
  them in 1934, or sold, restituted and sold again).
