-- Quotes cache on each checkout pod. Refreshed every 10 s from the liquidity providers.
CREATE TABLE currency (
  code     TEXT PRIMARY KEY,      -- ISO 4217
  name     TEXT NOT NULL,
  decimals INTEGER NOT NULL
);

-- One row per provider and direction: 1 unit of base buys `rate` units of quote.
CREATE TABLE quote (
  base      TEXT NOT NULL REFERENCES currency(code),
  quote     TEXT NOT NULL REFERENCES currency(code),
  rate      REAL NOT NULL,
  provider  TEXT NOT NULL,
  quoted_at TEXT NOT NULL,
  PRIMARY KEY (base, quote, provider)
);

-- Currencies compliance has put on the restricted list.
CREATE TABLE restricted_currency (
  code   TEXT PRIMARY KEY REFERENCES currency(code),
  reason TEXT NOT NULL,
  since  TEXT NOT NULL
);
