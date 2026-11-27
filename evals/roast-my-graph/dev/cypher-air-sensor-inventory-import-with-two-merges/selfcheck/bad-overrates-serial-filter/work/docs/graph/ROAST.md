# Review

Two problems: silent data loss from the serial filter (critical) and the site MERGE on nulls.

## Device.serial (critical)

Problem: WITH row WHERE row.serial IS NOT NULL silently discards feed rows: silent data loss.

Fix: Load every row and flag the ones without serial.

## site_code (medium)

Problem: Null site_code fails the MERGE for depot devices.

Fix: Make the Site MERGE conditional.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
