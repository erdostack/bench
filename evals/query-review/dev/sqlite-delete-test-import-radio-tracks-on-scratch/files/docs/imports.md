# Imports

Every row an import creates carries `import_batch`: `IMP-<mmdd>` for a real import, `IMP-TEST-<mmdd>` for a
test run of the import script (test runs only ever go to scratch). Hand-entered rows have NULL.

A track created by an import has one `by_artist` edge, one `on_release` edge and, if it was added to a
rotation, one `in_rotation` edge. An import reuses an artist or release that already exists and creates the
ones that do not, tagged with its batch.
