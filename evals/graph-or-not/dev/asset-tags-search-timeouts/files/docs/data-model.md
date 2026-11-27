# Data model

_Last updated 2025-01-14._

| Table | What it holds |
|---|---|
| `assets` | one row per picture: title, photographer, `taken_on`, rights |
| `tags` | one row per label (`name` is unique) |
| `asset_tags` | which tags an asset has (`asset_id`, `tag_id`) |
| `collections` | hand-picked sets of assets for a story |

Searching by tag joins `asset_tags` to `assets`.
