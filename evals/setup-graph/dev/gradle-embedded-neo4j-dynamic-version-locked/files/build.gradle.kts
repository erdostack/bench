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
    implementation("org.neo4j:neo4j:2026.+")
    testImplementation("org.junit.jupiter:junit-jupiter:5.12.2")
}

tasks.register<JavaExec>("runCypher") {
    description = "Run one .cypher file against build/graph-db: ./gradlew runCypher -Pfile=<path>"
    classpath = sourceSets["main"].runtimeClasspath
    mainClass = "org.pantry.RunCypher"
    args(providers.gradleProperty("file").getOrElse(""))
}

tasks.register<JavaExec>("seed") {
    classpath = sourceSets["main"].runtimeClasspath
    mainClass = "org.pantry.Seed"
}

tasks.test {
    useJUnitPlatform()
}
