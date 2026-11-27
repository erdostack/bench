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
    implementation("org.neo4j.driver:neo4j-java-driver:6.+")
    testImplementation("org.testcontainers:neo4j:1.21.3")
    testImplementation("org.junit.jupiter:junit-jupiter:5.12.2")
}

tasks.withType<Test>().configureEach {
    useJUnitPlatform()
    systemProperty("graph.image", providers.gradleProperty("graphImage").get())
    systemProperty("neo4j.accept.license", "yes")
}

tasks.register<Test>("adhoc") {
    description = "Run one query file against the seeded container: ./gradlew adhoc -Pcypher=<path>"
    testClassesDirs = sourceSets["test"].output.classesDirs
    classpath = sourceSets["test"].runtimeClasspath
    filter.includeTestsMatching("org.stagehand.AdHocQuery")
    systemProperty("query.file", providers.gradleProperty("cypher").getOrElse(""))
    outputs.upToDateWhen { false }
}

tasks.test {
    filter.excludeTestsMatching("org.stagehand.AdHocQuery")
}
