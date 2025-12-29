package uz.yalla.design.theme

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
import uz.yalla.design.color.ColorScheme
import uz.yalla.design.color.LocalColorScheme
import uz.yalla.design.color.dark
import uz.yalla.design.color.light
import uz.yalla.design.font.FontScheme
import uz.yalla.design.font.LocalFontScheme
import uz.yalla.design.font.rememberFontScheme

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

object System {
    val color: ColorScheme
        @Composable
        get() = LocalColorScheme.current

    val font: FontScheme
        @Composable
        get() = LocalFontScheme.current
}
