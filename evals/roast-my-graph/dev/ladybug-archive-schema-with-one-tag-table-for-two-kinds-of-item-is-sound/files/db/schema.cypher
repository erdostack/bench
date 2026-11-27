CREATE NODE TABLE Article(
    id STRING PRIMARY KEY,
    slug STRING,
    title STRING,
    section STRING,
    words INT64,
    published DATE
);

CREATE NODE TABLE Episode(
    id STRING PRIMARY KEY,
    title STRING,
    show STRING,
    duration_s INT64,
    audio_path STRING,
    published DATE
);

CREATE NODE TABLE Person(
    staff_no STRING PRIMARY KEY,
    name STRING,
    role STRING
);

CREATE NODE TABLE Tag(
    slug STRING PRIMARY KEY,
    label STRING,
    kind STRING
);

CREATE REL TABLE TaggedWith(FROM Article TO Tag, FROM Episode TO Tag);
CREATE REL TABLE MadeBy(FROM Article TO Person, FROM Episode TO Person, credit STRING);
