Added reports/lapsed.sql: active volunteers with no shift dated after :as_of minus 90 days and on or before :as_of,
including volunteers who never did a shift, ordered by name. Run it with `python -m rota.report lapsed as_of=2026-11-20`.
