UNWIND $researchers AS r
MERGE (x:Researcher {orcid: r.orcid})
  SET x.name = r.name, x.faculty = r.faculty;
