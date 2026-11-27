CREATE NODE TABLE Reader(
    id INT64 PRIMARY KEY,
    handle STRING,
    joined DATE
);

CREATE NODE TABLE Book(
    isbn STRING PRIMARY KEY,
    title STRING,
    year INT64
);

CREATE NODE TABLE Genre(
    slug STRING PRIMARY KEY,
    label STRING
);

CREATE REL TABLE Rated(FROM Reader TO Book, stars INT64, rated_on DATE);
CREATE REL TABLE InGenre(FROM Book TO Genre);
CREATE REL TABLE Follows(FROM Reader TO Reader, since DATE);
