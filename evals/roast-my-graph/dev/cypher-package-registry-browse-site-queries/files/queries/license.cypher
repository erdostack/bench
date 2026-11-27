// name: license_page
MATCH (l:License {spdx: $spdx})
RETURN l.name AS name, l.package_count AS packages;
