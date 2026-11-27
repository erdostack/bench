Run as it was, tonight's job would start again at sheet row 1 and write the 17,085 edges from rows 1-18,000
a second time: performed_on has no unique key, so nothing stops it. I changed the insert to skip a sheet
credit whose sessions edge (same artist, recording *and role*) already exists. The role matters: about
2,000 recordings have one artist in two roles, and some of those pairs straddle row 18,000, so checking
only artist+recording would drop the second role. On a copy of var/tonearm.db it adds the 11,380 missing
edges; a second run adds 0; killed mid-run and restarted it still ends with each edge once. Still 2,000
sheet rows per commit. I left var/tonearm.db as it was. Check with
`SELECT artist_id, recording_id, role, count(*) FROM performed_on GROUP BY 1,2,3 HAVING count(*) > 1`.
