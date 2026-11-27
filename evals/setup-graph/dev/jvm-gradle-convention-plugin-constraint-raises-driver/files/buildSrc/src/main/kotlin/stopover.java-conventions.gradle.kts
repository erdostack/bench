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
    constraints {
        implementation("org.neo4j.driver:neo4j-java-driver:5.28.1") {
            because("minimum client version from docs/platform-baseline.md")
        }
    }
}

tasks.withType<Test>().configureEach {
    useJUnitPlatform()
}
