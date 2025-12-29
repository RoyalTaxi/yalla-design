package uz.yalla.uikit.color

import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color

// Light Theme Colors
val LightTextBase = Color(0xFF101828)
val LightTextSubtle = Color(0xFF98A2B3)
val LightTextLink = Color(0xFF562DF8)
val LightTextRed = Color(0xFFF42500)
val LightTextWhite = Color(0xFFFFFFFF)

val LightBackgroundBase = Color(0xFFFFFFFF)
val LightBackgroundBrandBase = Color(0xFF562DF8)
val LightBackgroundSecondary = Color(0xFFF7F7F7)
val LightBackgroundTertiary = Color(0xFFE9EAEA)

val LightBorderDisabled = Color(0xFFE4E7EC)
val LightBorderFilled = Color(0xFF101828)
val LightBorderWhite = Color(0xFFFFFFFF)
val LightBorderError = Color(0xFFF42500)

val LightButtonActive = Color(0xFF562DF8)
val LightButtonDisabled = Color(0xFFC8CBFA)
val LightButtonSecondary = Color(0xFFF7F7F7)
val LightButtonTertiary = Color(0xFF101828)
val LightButtonDisabledTertiary = Color(0xFFCBD2E1)

val LightIconWhite = Color(0xFFFFFFFF)
val LightIconBase = Color(0xFF101828)
val LightIconSecondary = Color(0xFF562DF8)
val LightIconDisabled = Color(0xFFC8CBFA)
val LightIconRed = Color(0xFFF42500)
val LightIconSubtle = Color(0xFF98A2B3)

// Dark Theme Colors
val DarkTextBase = Color(0xFFFFFFFF)
val DarkTextSubtle = Color(0xFF747C8B)
val DarkTextLink = Color(0xFF562DF8)
val DarkTextRed = Color(0xFFF42500)
val DarkTextWhite = Color(0xFFFFFFFF)

val DarkBackgroundBase = Color(0xFF1A1A20)
val DarkBackgroundBrandBase = Color(0xFF562DF8)
val DarkBackgroundSecondary = Color(0xFF21222B)
val DarkBackgroundTertiary = Color(0xFF1D1D26)

val DarkBorderDisabled = Color(0xFF383843)
val DarkBorderFilled = Color(0xFFFFFFFF)
val DarkBorderWhite = Color(0xFFFFFFFF)
val DarkBorderError = Color(0xFFF42500)

val DarkButtonActive = Color(0xFF562DF8)
val DarkButtonDisabled = Color(0xFF2C2D34)
val DarkButtonSecondary = Color(0xFFF7F7F7)
val DarkButtonTertiary = Color(0xFFFFFFFF)
val DarkButtonDisabledTertiary = Color(0xFFCBD2E1)

val DarkIconWhite = Color(0xFFFFFFFF)
val DarkIconBase = Color(0xFFFFFFFF)
val DarkIconSecondary = Color(0xFF562DF8)
val DarkIconDisabled = Color(0xFF2C2D34)
val DarkIconRed = Color(0xFFF42500)
val DarkIconSubtle = Color(0xFF98A2B3)

// Accent Colors
val PinkSun = Color(0xFFFF234B)
val Color1 = Color(0xFFFFD1D2)
val Color2 = Color(0xFFCADDFF)
val Color3 = Color(0xFFFFDFAB)
val Color4 = Color(0xFFA7FFF9)
val Color5 = Color(0xFFD6C8FF)

// Gradients
val SplashBackground = Brush.verticalGradient(
    colors = listOf(
        Color(0xFF7957FF),
        Color(0xFF562DF8),
        Color(0xFF3812CE)
    ),
    startY = 0f,
    endY = 1000f
)

val SunsetNight = Brush.linearGradient(listOf(Color(0xFFFF234B), Color(0xFF2F00EC)))
