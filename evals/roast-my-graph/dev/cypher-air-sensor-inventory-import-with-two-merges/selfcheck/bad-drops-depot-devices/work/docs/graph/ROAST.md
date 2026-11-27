# Review

Filter out rows without site_code along with the serial-less ones; then the MERGE can't fail.

## import_devices.cypher (high)

Problem: Null site_code makes the Site MERGE fail.

Fix: Add AND row.site_code IS NOT NULL to the WHERE so incomplete rows are skipped.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
