# Changelog

## 2026-11-23
- jobs/backfill_image_components: count each component once per image. An SBOM lists a component once
  per layer that contains it, so the first version linked an image to the same component two or three
  times and counted every line. Now uses DISTINCT.

## 2026-11-21
- jobs/backfill_image_components: new job, fills image_component and image.component_count from
  sbom_entry for every image.
