package org.coldchain.it.support;

import org.testcontainers.utility.DockerImageName;
import org.testcontainers.utility.ImageNameSubstitutor;

/**
 * Keeps every container on the release line the hosted graph runs, so a test never passes on a
 * server we no longer have. Other images pass through unchanged.
 */
public final class ReleaseLineImages extends ImageNameSubstitutor {
    private static final DockerImageName GRAPH = DockerImageName.parse("neo4j:2026.02.2-community");

    @Override
    public DockerImageName apply(DockerImageName original) {
        return "neo4j".equals(original.getRepository()) ? GRAPH : original;
    }

    @Override
    protected String getDescription() {
        return "release-line images";
    }
}
