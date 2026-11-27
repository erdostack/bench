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
    implementation("org.neo4j.driver:neo4j-java-driver:[5.20,7.0)")
    testImplementation("org.junit.jupiter:junit-jupiter:5.+")
}

tasks.register<JavaExec>("cypher") {
    description = "Run one .cypher file: ./gradlew cypher -Pfile=<path>"
    classpath = sourceSets["main"].runtimeClasspath
    mainClass = "org.stopwatch.Cypher"
    args(providers.gradleProperty("file").getOrElse(""))
}

tasks.test {
    useJUnitPlatform()
}
