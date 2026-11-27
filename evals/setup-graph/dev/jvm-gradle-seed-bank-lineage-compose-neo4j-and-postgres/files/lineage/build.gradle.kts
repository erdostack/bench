plugins { java }

repositories { mavenCentral() }

java { toolchain { languageVersion = JavaLanguageVersion.of(21) } }

dependencyLocking { lockAllConfigurations() }

dependencies {
    implementation("org.neo4j.driver:neo4j-java-driver:5.+")
}

tasks.register<JavaExec>("cypher") {
    group = "graph"
    description = "Runs one saved Cypher file: ./gradlew :lineage:cypher -Pfile=queries/x.cypher"
    classpath = sourceSets["main"].runtimeClasspath
    mainClass = "org.seedvault.lineage.Cypher"
    workingDir = rootDir
    args(providers.gradleProperty("file").get())
}

tasks.register<JavaExec>("load") {
    group = "graph"
    classpath = sourceSets["main"].runtimeClasspath
    mainClass = "org.seedvault.lineage.Load"
    workingDir = rootDir
}
