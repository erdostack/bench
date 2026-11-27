plugins {
    java
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    mavenCentral()
}

dependencyLocking {
    lockAllConfigurations()
}

dependencies {
    // Memgraph speaks Bolt, so the Neo4j Java driver works as its client.
    implementation("org.neo4j.driver:neo4j-java-driver:5.+")
    testImplementation("org.junit.jupiter:junit-jupiter:5.12.2")
}

tasks.register<JavaExec>("query") {
    description = "Run one .cypher file: ./gradlew query -Pfile=<path>"
    classpath = sourceSets["main"].runtimeClasspath
    mainClass = "org.gridline.Query"
    args(providers.gradleProperty("file").getOrElse(""))
}
