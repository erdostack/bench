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

configurations.all {
    resolutionStrategy {
        // hold the embedded engine until data/book-db is migrated (issue 41)
        force("org.neo4j:neo4j:5.26.24")
    }
}

dependencies {
    implementation("org.neo4j:neo4j:2026.05.0")
    testImplementation("org.junit.jupiter:junit-jupiter:5.12.2")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

tasks.register<JavaExec>("cypher") {
    description = "Run one .cypher file read-only against data/book-db: ./gradlew cypher -Pfile=<path>"
    classpath = sourceSets["main"].runtimeClasspath
    mainClass = "org.openingbook.Cypher"
    args(providers.gradleProperty("file").getOrElse(""))
}

tasks.test {
    useJUnitPlatform()
}
