# Changelog

## 2025-06-02
- The image now builds its own libsqlite3 (see Dockerfile) instead of linking Debian's, so the engine
  no longer changes when the base image does.

## 2025-02-11
- `stopq` takes positional arguments after the flags and binds them as `?1`, `?2`, ...

## 2024-11-20
- First version: `link` table, `reachable_within.sql`.
