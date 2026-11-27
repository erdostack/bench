# pkgatlas

Search and browse site over a public package registry's metadata. Neo4j 5.26.

    model/model.md            labels and relationships
    model/schema.cypher       constraints
    queries/package.cypher    package page
    queries/license.cypher    license page
    queries/nightly.cypher    nightly maintenance

## Sizes

| Thing | Count |
|---|---|
| Package | 2.6 million |
| License | 410; MIT 1.52 million packages, ISC 610,000, Apache-2.0 290,000; 300 licenses have under 100 |
| Maintainer | 1.1 million |
| Package.category | 64 categories, the largest ("web") 410,000 packages |

## Traffic

Package page: about 900 views a second at peak. Each view runs `package_page` and, since the last
release, `related_packages` for the new "Similar packages" box. License page: about 2 a second.
`nightly.cypher` runs once a night.
