# checkout-fx

Currency conversion for checkout. Each checkout pod keeps a SQLite quotes cache (`db/schema.sql`) that a sidecar
refreshes every 10 seconds from the liquidity providers.

- `fx/route.py`: rates and conversion.

Python 3.11. The pod image has the standard library and networkx.
