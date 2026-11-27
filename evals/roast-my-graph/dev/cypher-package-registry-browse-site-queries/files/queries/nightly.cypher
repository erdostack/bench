// name: refresh_license_counts
MATCH (l:License)
SET l.package_count = COUNT { (l)<-[:LICENSED_UNDER]-(:Package) };
