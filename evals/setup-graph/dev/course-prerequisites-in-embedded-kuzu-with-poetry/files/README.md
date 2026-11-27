# prereq

Course-prerequisite graph for the faculty's timetabling office. Courses are nodes, "requires" and
"corequisite" are relationships, and the questions are walks: everything a student must have passed
before taking X, or courses nobody can reach.

The database is embedded Kuzu 0.11.3: it is a directory, `db/courses`, opened in process by the Python
package. There is no server to start.

    poetry install
    make load            # rebuilds db/courses from data/*.csv
    make query F=queries/all_prereqs.cypher CODE=MATH201

Queries are Cypher. `make query` opens the database read-only.
