"""Load the unit tree into Neo4j for the reporting pack."""
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687")
