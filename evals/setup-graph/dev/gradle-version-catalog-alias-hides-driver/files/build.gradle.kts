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
    implementation(libs.graph.client)
    runtimeOnly(libs.slf4j.simple)
    testImplementation(libs.junit.jupiter)
}

tasks.register<JavaExec>("cypher") {
    description = "Run one .cypher file: ./gradlew cypher -Pfile=<path>"
    classpath = sourceSets["main"].runtimeClasspath
    mainClass = "org.ferryboard.Cypher"
    args(providers.gradleProperty("file").getOrElse(""))
}

tasks.test {
    useJUnitPlatform()
}
