"""Apply one data change. Usage: python3 tools/apply.py <uri> <file>"""
import sys
from pathlib import Path

from neo4j import GraphDatabase

if __name__ == "__main__":
    with GraphDatabase.driver(sys.argv[1]) as driver, driver.session(database="boxtrail") as session:
        print(session.run(Path(sys.argv[2]).read_text()).consume().counters)
