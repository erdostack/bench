# Model

- `Package {name, description, category, latest_version, weekly_downloads}`
- `License {spdx, name, package_count}`; package_count is refreshed nightly
- `Maintainer {handle}`

- `(:Package)-[:LICENSED_UNDER]->(:License)`, one per package
- `(:Maintainer)-[:MAINTAINS]->(:Package)`
- `(:Package)-[:DEPENDS_ON]->(:Package)`
