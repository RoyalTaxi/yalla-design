# Yalla Design

A Kotlin Multiplatform design system library for Android and iOS applications.

## Installation

Add the GitHub Packages repository and dependency to your project:

```kotlin
// settings.gradle.kts
dependencyResolutionManagement {
    repositories {
        maven {
            url = uri("https://maven.pkg.github.com/RoyalTaxi/yalla-design")
            credentials {
                username = project.findProperty("gpr.user") as String? ?: System.getenv("GITHUB_ACTOR")
                password = project.findProperty("gpr.key") as String? ?: System.getenv("GITHUB_TOKEN")
            }
        }
    }
}

// build.gradle.kts
dependencies {
    implementation("uz.yalla:design:1.0.0")
}
```

## Usage

### Theme Setup

Wrap your app content with `YallaTheme`:

```kotlin
@Composable
fun App() {
    YallaTheme {
        // Your content
    }
}
```

With custom dark mode handling:

```kotlin
@Composable
fun App() {
    val isDark = isSystemInDarkTheme()

    YallaTheme(isDark = isDark) {
        // Your content
    }
}
```

### Accessing Design Tokens

Use the `System` object to access colors and fonts:

```kotlin
@Composable
fun MyComponent() {
    Text(
        text = "Hello",
        color = System.color.textBase,
        style = System.font.body.base.medium
    )
}
```

### Color System

Available color categories:
- **Text**: `textBase`, `textSubtle`, `textLink`, `textRed`, `textWhite`
- **Background**: `backgroundBase`, `backgroundBrandBase`, `backgroundSecondary`, `backgroundTertiary`
- **Border**: `borderDisabled`, `borderFilled`, `borderWhite`, `borderError`
- **Button**: `buttonActive`, `buttonDisabled`, `buttonSecondary`, `buttonTertiary`
- **Icon**: `iconWhite`, `iconBase`, `iconSecondary`, `iconDisabled`, `iconRed`, `iconSubtle`
- **Accent**: `pinkSun`, `color1`-`color5`
- **Gradients**: `splashBackground`, `sunsetNight`

### Font System

Typography scale:
- **Title**: `xLarge` (30sp), `large` (22sp), `base` (20sp)
- **Body**: `large`, `base`, `small` - each with `regular`, `medium`, `bold` weights
- **Caption**: 13sp medium weight
- **Custom**: `carNumber` (for vehicle plates)

## Custom Themes

Create custom color schemes:

```kotlin
val customColors = light(
    buttonActive = Color(0xFF00FF00),
    textBase = Color(0xFF333333)
)

YallaTheme(colorScheme = customColors) {
    // Content with custom colors
}
```

## License

Copyright 2024 Yalla. All rights reserved.
