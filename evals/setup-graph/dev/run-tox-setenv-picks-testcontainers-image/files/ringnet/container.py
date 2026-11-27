"""Starts the throwaway Memgraph container that tests and ad-hoc queries use."""
import os
import time

from neo4j import GraphDatabase
from testcontainers.core.container import DockerContainer

IMAGE = os.environ.get("MEMGRAPH_IMAGE", "memgraph/memgraph:2.21.0")


def start() -> DockerContainer:
    container = DockerContainer(IMAGE).with_exposed_ports(7687)
    container.start()
    deadline = time.time() + 60
    while True:
        try:
            with GraphDatabase.driver(bolt_uri(container), auth=None) as driver:
                driver.verify_connectivity()
            return container
        except Exception:
            if time.time() > deadline:
                container.stop()
                raise
            time.sleep(1)


def bolt_uri(container: DockerContainer) -> str:
    return f"bolt://{container.get_container_host_ip()}:{container.get_exposed_port(7687)}"
