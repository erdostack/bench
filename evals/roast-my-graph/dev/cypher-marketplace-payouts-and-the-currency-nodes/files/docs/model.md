# Why Currency is a node

Every amount is stored in minor units, and the number of decimals depends on the currency (JPY has 0,
EUR 2, a few have 3). Keeping that on one Currency node means payments only carry the code via the
relationship and the app reads decimals from one place. We always go payment -> currency, never the
other way, and currencies are never deleted.
