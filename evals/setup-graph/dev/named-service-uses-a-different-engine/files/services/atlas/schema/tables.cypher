CREATE NODE TABLE Junction(ref STRING, ward STRING, PRIMARY KEY (ref));
CREATE REL TABLE PATH(FROM Junction TO Junction, metres INT64, steps BOOLEAN, surface STRING);
