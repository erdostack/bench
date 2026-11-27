plugins {
    application
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
    implementation("org.neo4j.driver:neo4j-java-driver:5.28.1")
    testImplementation("org.junit.jupiter:junit-jupiter:5.12.2")
}

application {
    mainClass = "shop.recs.Main"
}
