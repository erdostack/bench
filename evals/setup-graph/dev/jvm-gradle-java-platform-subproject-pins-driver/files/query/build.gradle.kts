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
    implementation(platform(project(":platform")))
    implementation("org.neo4j.driver:neo4j-java-driver")
    runtimeOnly("org.slf4j:slf4j-simple")
}

application {
    mainClass = "org.commitnet.query.Main"
}

tasks.named<JavaExec>("run") {
    workingDir = rootDir
}
