# Upgrade plan (next quarter)

1. Move the server to 2026.05.0 in compose.yaml.
2. Then lift the driver to 6.1.0 (`./gradlew dependencies --write-locks`).
3. Re-run the journey tests against both.

Nothing here has been done yet.
