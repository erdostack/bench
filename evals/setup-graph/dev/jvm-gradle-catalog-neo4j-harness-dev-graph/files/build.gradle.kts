plugins {
    alias(libs.plugins.kotlin.jvm)
    application
}

repositories { mavenCentral() }

kotlin { jvmToolchain(21) }

dependencyLocking {
    lockAllConfigurations()
}

dependencies {
    implementation(libs.neo4j.harness)
    implementation(libs.neo4j.driver)
    testImplementation(libs.junit)
}

application {
    mainClass.set("org.seedswap.DevGraphKt")
}

tasks.test { useJUnitPlatform() }
