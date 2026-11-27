# Model

`nodes.kind`: `order`, `customer`, `shop`, `machine`. `nodes.ref` is unique: `SW-<year>-<n>` for real
orders, `C-<n>` for real customers, `LD-<nn>` shops. The load-test scripts create customers `LTC-<n>` and
orders `LT-<n>` on scratch.

| edge kind | src | dst |
|---|---|---|
| `placed_by` | order | customer |
| `taken_at` | order | shop |
| `washed_in` | order | machine (one or two) |

There are no foreign keys.
