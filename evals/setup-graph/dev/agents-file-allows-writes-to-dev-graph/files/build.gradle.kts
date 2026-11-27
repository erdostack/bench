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
    testImplementation("org.junit.jupiter:junit-jupiter:5.+")
}

tasks.register<JavaExec>("cypher") {
    description = "Run one .cypher file: ./gradlew cypher -Pfile=<path>"
    classpath = sourceSets["main"].runtimeClasspath
    mainClass = "dev.dockyard.CypherFile"
    args(providers.gradleProperty("file").getOrElse(""))
}

tasks.register<JavaExec>("resetGraph") {
    description = "Wipe the dev database and reload fixtures/"
    classpath = sourceSets["main"].runtimeClasspath
    mainClass = "dev.dockyard.ResetGraph"
}

tasks.test {
    useJUnitPlatform()
}
