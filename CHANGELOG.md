# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-06

### Changed
- **Resources Migration**
  - Migrated all font resources to `yalla-resources` library
  - Now depends on `uz.yalla:resources:1.0.0`
  - Fonts are now loaded from yalla-resources instead of local composeResources

### Removed
- Local composeResources directory (fonts moved to yalla-resources)

## [1.0.0] - 2024-12-29

### Added
- Initial stable release
- `YallaTheme` composable for theming applications
- `ColorScheme` with light and dark theme support
- `FontScheme` with title, body, and custom typography
- Platform-specific fonts (Roboto for Android, SF Pro for iOS)
- `System` object for accessing design tokens
- Compose Multiplatform resources integration

### Changed
- Renamed package from `uz.yalla.uikit` to `uz.yalla.design`
- Moved `SystemBarColors` to separate platform module

### Removed
- `SystemBarColors` (moved to platform module)
- `LocalCustomColorScheme` alias (use `LocalColorScheme` directly)
