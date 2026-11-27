CREATE NODE TABLE Sailor(
    id INT64 PRIMARY KEY,
    full_name STRING,
    rank STRING
);

CREATE NODE TABLE Vessel(
    imo STRING PRIMARY KEY,
    name STRING,
    flag STRING
);

CREATE NODE TABLE Port(
    code STRING PRIMARY KEY,
    name STRING,
    country STRING
);

CREATE NODE TABLE CrewAssignment(
    id SERIAL PRIMARY KEY,
    sailor_id INT64,
    vessel_imo STRING,
    role STRING,
    signed_on DATE,
    signed_off DATE
);

CREATE REL TABLE HasAssignment(FROM Sailor TO CrewAssignment);
CREATE REL TABLE AssignmentOn(FROM CrewAssignment TO Vessel);

CREATE NODE TABLE Voyage(
    id INT64 PRIMARY KEY,
    vessel_imo STRING,
    origin_port_code STRING,
    dest_port_code STRING,
    departed DATE,
    arrived DATE
);
