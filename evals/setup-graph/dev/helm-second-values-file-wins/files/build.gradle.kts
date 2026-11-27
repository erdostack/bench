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

dependencies {
    implementation("org.neo4j.driver:neo4j-java-driver:6.1.0")
    testImplementation("org.junit.jupiter:junit-jupiter:5.12.2")
}

tasks.register<JavaExec>("cypher") {
    description = "Run one .cypher file: ./gradlew cypher -Pfile=<path>"
    classpath = sourceSets["main"].runtimeClasspath
    mainClass = "org.pollen.Cypher"
    args(providers.gradleProperty("file").getOrElse(""))
}

tasks.register<JavaExec>("seed") {
    classpath = sourceSets["main"].runtimeClasspath
    mainClass = "org.pollen.Seed"
}
