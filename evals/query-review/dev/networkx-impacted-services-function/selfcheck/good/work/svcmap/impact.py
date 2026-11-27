"""What an outage affects."""
import networkx as nx


def impacted_by(G, service):
    """Every service that calls `service`, directly or through other services, sorted; not `service` itself."""
    return sorted(nx.ancestors(G, service) - {service})
