"""Runtime settings, all from the environment."""
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    graph_uri: str = os.environ.get("GRAPH_URI", "bolt://localhost:7687")
    graph_user: str = "neo4j"
    graph_password: str = os.environ.get("GRAPH_PASSWORD", "")
    min_transfer_minutes: int = int(os.environ.get("MIN_TRANSFER_MINUTES", "12"))


settings = Settings()
