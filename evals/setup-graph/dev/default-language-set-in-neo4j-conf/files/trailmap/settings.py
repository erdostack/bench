"""Connection settings, read from the environment (config/local is exported by the Makefile)."""
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    uri: str
    user: str
    password: str


def load() -> Settings:
    return Settings(uri=os.environ.get("GRAPH_URI", "bolt://localhost:7687"),
                    user=os.environ.get("GRAPH_USER", "neo4j"),
                    password=os.environ["GRAPH_PASSWORD"])
