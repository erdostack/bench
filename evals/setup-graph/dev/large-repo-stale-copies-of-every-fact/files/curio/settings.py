"""Settings from the environment. Defaults suit `make up`."""
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    uri: str = os.environ.get("CURIO_GRAPH_URI", "bolt://localhost:7687")
    user: str = os.environ.get("CURIO_GRAPH_USER", "neo4j")
    password: str = os.environ.get("CURIO_GRAPH_PASSWORD", "")
    database: str = os.environ.get("CURIO_GRAPH_DATABASE", "neo4j")
    # the loader overrides this; everything else reads
    access_mode: str = os.environ.get("CURIO_GRAPH_ACCESS_MODE", "READ")


def load() -> Settings:
    return Settings()
