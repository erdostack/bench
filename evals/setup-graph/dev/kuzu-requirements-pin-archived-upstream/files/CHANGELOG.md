# Changelog

## 0.6.0

- `query` prints results as a table instead of raw tuples.
- New saved query: `queries/swap_chain.cypher`.

## 0.5.2

- Pinned `kuzu` to 0.11.3 in `requirements.txt`. Upstream archived the repository in October 2025, so this is
  the last release and no fixes will follow. Staying on it for now; look at the LadybugDB fork when there is time.
- `load` now creates `var/` if it is missing.

## 0.5.0

- Substitutions (`SWAPS_FOR`) and the "almost cookable" query.

## 0.4.0

- First version with an embedded database instead of JSON files.
