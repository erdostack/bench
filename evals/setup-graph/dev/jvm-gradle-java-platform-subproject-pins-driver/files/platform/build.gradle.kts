plugins {
    `java-platform`
}

dependencies {
    constraints {
        api("org.neo4j.driver:neo4j-java-driver:6.1.0")
        api("org.slf4j:slf4j-simple:2.0.17")
    }
}
