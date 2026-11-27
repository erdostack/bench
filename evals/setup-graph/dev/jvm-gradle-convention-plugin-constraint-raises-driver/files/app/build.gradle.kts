plugins {
    id("stopover.java-conventions")
}

dependencies {
    implementation("org.neo4j.driver:neo4j-java-driver:5.20.0")
    testImplementation("org.junit.jupiter:junit-jupiter:5.12.2")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

tasks.register<JavaExec>("cypher") {
    description = "Run one .cypher file: ./gradlew :app:cypher -Pfile=<path>"
    classpath = sourceSets["main"].runtimeClasspath
    mainClass = "org.stopover.Cypher"
    workingDir = rootDir
    args(providers.gradleProperty("file").getOrElse(""))
}
