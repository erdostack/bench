plugins {
    application
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.neo4j.driver:neo4j-java-driver:5.+")
    implementation("info.picocli:picocli:4.7.6")
}

dependencyLocking {
    lockAllConfigurations()
}

java {
    toolchain { languageVersion = JavaLanguageVersion.of(21) }
}

application {
    mainClass = "org.orchard.Query"
}
