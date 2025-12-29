package uz.yalla.uikit.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material.ripple.RippleAlpha
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.LocalRippleConfiguration
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.RippleConfiguration
import androidx.compose.material3.darkColorScheme as materialDarkColorScheme
import androidx.compose.material3.lightColorScheme as materialLightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.ui.graphics.Color
import uz.yalla.uikit.color.ColorScheme
import uz.yalla.uikit.color.LocalColorScheme
import uz.yalla.uikit.color.dark
import uz.yalla.uikit.color.light
import uz.yalla.uikit.font.FontScheme
import uz.yalla.uikit.font.LocalFontScheme
import uz.yalla.uikit.font.rememberFontScheme
import uz.yalla.uikit.system.SystemBarColors

/**
 * Yalla UI Kit Theme.
 *
 * This is the main theme composable for the Yalla design system.
 * It provides colors, typography, and Material 3 theming.
 *
 * @param isDark Whether to use dark theme. Defaults to system setting.
 * @param colorScheme Optional custom color scheme. If not provided, uses default light/dark scheme.
 * @param fontScheme Optional custom font scheme. If not provided, uses default fonts.
 * @param content The content to wrap with the theme.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun YallaTheme(
    isDark: Boolean = isSystemInDarkTheme(),
    colorScheme: ColorScheme = if (isDark) dark() else light(),
    fontScheme: FontScheme = rememberFontScheme(),
    content: @Composable () -> Unit
) {
    val rippleConfiguration = RippleConfiguration(
        color = if (isDark) Color.White else Color.Black,
        rippleAlpha = RippleAlpha(
            pressedAlpha = 0.12f,
            focusedAlpha = 0.08f,
            draggedAlpha = 0.12f,
            hoveredAlpha = 0.08f
        )
    )

    val materialColorScheme = if (isDark) {
        materialDarkColorScheme(
            primary = colorScheme.buttonActive,
            onPrimary = colorScheme.textWhite,
            secondary = colorScheme.buttonSecondary,
            tertiary = colorScheme.buttonTertiary,
            background = colorScheme.backgroundBase,
            surface = colorScheme.backgroundSecondary,
            error = colorScheme.textRed,
            onBackground = colorScheme.textBase,
            onSurface = colorScheme.textBase
        )
    } else {
        materialLightColorScheme(
            primary = colorScheme.buttonActive,
            onPrimary = colorScheme.textWhite,
            secondary = colorScheme.buttonSecondary,
            tertiary = colorScheme.buttonTertiary,
            background = colorScheme.backgroundBase,
            surface = colorScheme.backgroundSecondary,
            error = colorScheme.textRed,
            onBackground = colorScheme.textBase,
            onSurface = colorScheme.textBase
        )
    }

    SystemBarColors(darkIcons = !isDark)

    CompositionLocalProvider(
        LocalColorScheme provides colorScheme,
        LocalFontScheme provides fontScheme,
        LocalRippleConfiguration provides rippleConfiguration
    ) {
        MaterialTheme(
            colorScheme = materialColorScheme,
            content = content
        )
    }
}

/**
 * Access the current Yalla design system values.
 */
object System {
    /**
     * The current color scheme provided by [YallaTheme].
     */
    val color: ColorScheme
        @Composable
        get() = LocalColorScheme.current

    /**
     * The current font scheme provided by [YallaTheme].
     */
    val font: FontScheme
        @Composable
        get() = LocalFontScheme.current
}
