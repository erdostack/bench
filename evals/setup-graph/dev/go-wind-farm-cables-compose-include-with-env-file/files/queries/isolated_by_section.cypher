// Turbines that lose every path to a substation when one cable section is opened.
MATCH (cut:Section {id: $section})
MATCH (t:Turbine)
WHERE NOT EXISTS {
  MATCH p = (t)-[:CABLE*1..40]-(:Substation)
  WHERE NONE(r IN relationships(p) WHERE r.section = cut.id OR r.normallyOpen)
}
RETURN t.id, t.string
ORDER BY t.string, t.id;
