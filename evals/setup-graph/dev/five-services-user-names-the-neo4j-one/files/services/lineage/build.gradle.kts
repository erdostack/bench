plugins {
    application
}

group = "io.tidepool"
version = "1.9.0"

java {
    toolchain { languageVersion = JavaLanguageVersion.of(21) }
}

repositories {
    mavenCentral()
}

dependencyLocking {
    lockAllConfigurations()
}

dependencies {
    implementation("org.neo4j.driver:neo4j-java-driver:6.+")
    implementation("io.javalin:javalin:6.+")
    runtimeOnly("org.slf4j:slf4j-simple:2.0.+")
    testImplementation(platform("org.junit:junit-bom:5.12.2"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

application {
    mainClass = "io.tidepool.lineage.Server"
}

tasks.register<JavaExec>("runQuery") {
    group = "application"
    description = "Run one saved query read-only: -Pfile=<path> [-Pparams=name=value,...]"
    classpath = sourceSets["main"].runtimeClasspath
    mainClass = "io.tidepool.lineage.RunQuery"
    args = listOfNotNull(findProperty("file") as String?, findProperty("params") as String?)
}

tasks.test {
    useJUnitPlatform()
}
