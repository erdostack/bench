# sbom-graph

Which open-source components ship inside which of our container images, built from the images' SBOMs.
SQLite (`var/sbom.db`), schema in `db/schema.sql`.

- `sbom_entry`: one row per component line of an image's SBOM, as imported.
- `image_component`: the image-to-component edges the vulnerability scanner walks; `image.component_count`
  is what the image pages show.
- `jobs/`: nightly jobs (`docs/jobs.md`). `python -m jobs <name>` runs one by hand.
