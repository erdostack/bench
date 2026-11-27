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
    implementation("org.neo4j.driver:neo4j-java-driver:5.+")
    implementation("org.neo4j:neo4j-cypher-dsl:2025.+")
}

tasks.register<JavaExec>("cypher") {
    classpath = sourceSets["main"].runtimeClasspath
    mainClass = "org.talkgraph.Cypher"
    args(providers.gradleProperty("file").getOrElse(""))
}
