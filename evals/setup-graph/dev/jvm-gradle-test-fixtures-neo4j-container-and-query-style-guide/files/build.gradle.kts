plugins {
    java
    `java-test-fixtures`
}

repositories { mavenCentral() }

java { toolchain { languageVersion.set(JavaLanguageVersion.of(21)) } }

dependencyLocking { lockAllConfigurations() }

dependencies {
    implementation("org.neo4j.driver:neo4j-java-driver:6.+")
    testFixturesApi("org.testcontainers:neo4j:1.21.3")
    testFixturesApi("org.neo4j.driver:neo4j-java-driver:6.+")
    testImplementation("org.junit.jupiter:junit-jupiter:5.12.2")
}

tasks.test {
    useJUnitPlatform { excludeTags("adhoc") }
}

// bin/q: ./gradlew adhoc -Pcypher=<file>
tasks.register<Test>("adhoc") {
    testClassesDirs = sourceSets.test.get().output.classesDirs
    classpath = sourceSets.test.get().runtimeClasspath
    useJUnitPlatform { includeTags("adhoc") }
    systemProperty("cypher.file", (findProperty("cypher") ?: "").toString())
    outputs.upToDateWhen { false }
    testLogging { showStandardStreams = true }
}
