package uz.yalla.uikit.color

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.runtime.structuralEqualityPolicy
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color

class ColorScheme(
    textBase: Color,
    textSubtle: Color,
    textLink: Color,
    textRed: Color,
    textWhite: Color,
    backgroundBase: Color,
    backgroundBrandBase: Color,
    backgroundSecondary: Color,
    backgroundTertiary: Color,
    borderDisabled: Color,
    borderFilled: Color,
    borderWhite: Color,
    borderError: Color,
    buttonActive: Color,
    buttonDisabled: Color,
    buttonSecondary: Color,
    buttonTertiary: Color,
    buttonDisabledTertiary: Color,
    iconWhite: Color,
    iconBase: Color,
    iconSecondary: Color,
    iconDisabled: Color,
    iconRed: Color,
    iconSubtle: Color,
    pinkSun: Color,
    splashBackground: Brush,
    sunsetNight: Brush,
    color1: Color,
    color2: Color,
    color3: Color,
    color4: Color,
    color5: Color
) {
    var textBase by mutableStateOf(textBase, structuralEqualityPolicy())
    var textSubtle by mutableStateOf(textSubtle, structuralEqualityPolicy())
    var textLink by mutableStateOf(textLink, structuralEqualityPolicy())
    var textRed by mutableStateOf(textRed, structuralEqualityPolicy())
    var textWhite by mutableStateOf(textWhite, structuralEqualityPolicy())
    var backgroundBase by mutableStateOf(backgroundBase, structuralEqualityPolicy())
    var backgroundBrandBase by mutableStateOf(backgroundBrandBase, structuralEqualityPolicy())
    var backgroundSecondary by mutableStateOf(backgroundSecondary, structuralEqualityPolicy())
    var backgroundTertiary by mutableStateOf(backgroundTertiary, structuralEqualityPolicy())
    var borderDisabled by mutableStateOf(borderDisabled, structuralEqualityPolicy())
    var borderFilled by mutableStateOf(borderFilled, structuralEqualityPolicy())
    var borderWhite by mutableStateOf(borderWhite, structuralEqualityPolicy())
    var borderError by mutableStateOf(borderError, structuralEqualityPolicy())
    var buttonActive by mutableStateOf(buttonActive, structuralEqualityPolicy())
    var buttonDisabled by mutableStateOf(buttonDisabled, structuralEqualityPolicy())
    var buttonSecondary by mutableStateOf(buttonSecondary, structuralEqualityPolicy())
    var buttonTertiary by mutableStateOf(buttonTertiary, structuralEqualityPolicy())
    var buttonDisabledTertiary by mutableStateOf(buttonDisabledTertiary, structuralEqualityPolicy())
    var iconWhite by mutableStateOf(iconWhite, structuralEqualityPolicy())
    var iconBase by mutableStateOf(iconBase, structuralEqualityPolicy())
    var iconSecondary by mutableStateOf(iconSecondary, structuralEqualityPolicy())
    var iconDisabled by mutableStateOf(iconDisabled, structuralEqualityPolicy())
    var iconRed by mutableStateOf(iconRed, structuralEqualityPolicy())
    var iconSubtle by mutableStateOf(iconSubtle, structuralEqualityPolicy())
    var pinkSun by mutableStateOf(pinkSun, structuralEqualityPolicy())
    var splashBackground by mutableStateOf(splashBackground, structuralEqualityPolicy())
    var sunsetNight by mutableStateOf(sunsetNight, structuralEqualityPolicy())
    var color1 by mutableStateOf(color1, structuralEqualityPolicy())
    var color2 by mutableStateOf(color2, structuralEqualityPolicy())
    var color3 by mutableStateOf(color3, structuralEqualityPolicy())
    var color4 by mutableStateOf(color4, structuralEqualityPolicy())
    var color5 by mutableStateOf(color5, structuralEqualityPolicy())

    fun copy(
        textBase: Color = this.textBase,
        textSubtle: Color = this.textSubtle,
        textLink: Color = this.textLink,
        textRed: Color = this.textRed,
        textWhite: Color = this.textWhite,
        backgroundBase: Color = this.backgroundBase,
        backgroundBrandBase: Color = this.backgroundBrandBase,
        backgroundSecondary: Color = this.backgroundSecondary,
        backgroundTertiary: Color = this.backgroundTertiary,
        borderDisabled: Color = this.borderDisabled,
        borderFilled: Color = this.borderFilled,
        borderWhite: Color = this.borderWhite,
        borderError: Color = this.borderError,
        buttonActive: Color = this.buttonActive,
        buttonDisabled: Color = this.buttonDisabled,
        buttonSecondary: Color = this.buttonSecondary,
        buttonTertiary: Color = this.buttonTertiary,
        buttonDisabledTertiary: Color = this.buttonDisabledTertiary,
        iconWhite: Color = this.iconWhite,
        iconBase: Color = this.iconBase,
        iconSecondary: Color = this.iconSecondary,
        iconDisabled: Color = this.iconDisabled,
        iconRed: Color = this.iconRed,
        iconSubtle: Color = this.iconSubtle,
        pinkSun: Color = this.pinkSun,
        splashBackground: Brush = this.splashBackground,
        sunsetNight: Brush = this.sunsetNight,
        color1: Color = this.color1,
        color2: Color = this.color2,
        color3: Color = this.color3,
        color4: Color = this.color4,
        color5: Color = this.color5
    ) = ColorScheme(
        textBase = textBase,
        textSubtle = textSubtle,
        textLink = textLink,
        textRed = textRed,
        textWhite = textWhite,
        backgroundBase = backgroundBase,
        backgroundBrandBase = backgroundBrandBase,
        backgroundSecondary = backgroundSecondary,
        backgroundTertiary = backgroundTertiary,
        borderDisabled = borderDisabled,
        borderFilled = borderFilled,
        borderWhite = borderWhite,
        borderError = borderError,
        buttonActive = buttonActive,
        buttonDisabled = buttonDisabled,
        buttonSecondary = buttonSecondary,
        buttonTertiary = buttonTertiary,
        buttonDisabledTertiary = buttonDisabledTertiary,
        iconWhite = iconWhite,
        iconBase = iconBase,
        iconSecondary = iconSecondary,
        iconDisabled = iconDisabled,
        iconRed = iconRed,
        iconSubtle = iconSubtle,
        pinkSun = pinkSun,
        splashBackground = splashBackground,
        sunsetNight = sunsetNight,
        color1 = color1,
        color2 = color2,
        color3 = color3,
        color4 = color4,
        color5 = color5
    )
}

fun light(
    textBase: Color = LightTextBase,
    textSubtle: Color = LightTextSubtle,
    textLink: Color = LightTextLink,
    textRed: Color = LightTextRed,
    textWhite: Color = LightTextWhite,
    backgroundBase: Color = LightBackgroundBase,
    backgroundBrandBase: Color = LightBackgroundBrandBase,
    backgroundSecondary: Color = LightBackgroundSecondary,
    backgroundTertiary: Color = LightBackgroundTertiary,
    borderDisabled: Color = LightBorderDisabled,
    borderFilled: Color = LightBorderFilled,
    borderWhite: Color = LightBorderWhite,
    borderError: Color = LightBorderError,
    buttonActive: Color = LightButtonActive,
    buttonDisabled: Color = LightButtonDisabled,
    buttonSecondary: Color = LightButtonSecondary,
    buttonTertiary: Color = LightButtonTertiary,
    buttonDisabledTertiary: Color = LightButtonDisabledTertiary,
    iconWhite: Color = LightIconWhite,
    iconBase: Color = LightIconBase,
    iconSecondary: Color = LightIconSecondary,
    iconDisabled: Color = LightIconDisabled,
    iconRed: Color = LightIconRed,
    iconSubtle: Color = LightIconSubtle,
    pinkSun: Color = PinkSun,
    splashBackground: Brush = SplashBackground,
    sunsetNight: Brush = SunsetNight,
    color1: Color = Color1,
    color2: Color = Color2,
    color3: Color = Color3,
    color4: Color = Color4,
    color5: Color = Color5
) = ColorScheme(
    textBase = textBase,
    textSubtle = textSubtle,
    textLink = textLink,
    textRed = textRed,
    textWhite = textWhite,
    backgroundBase = backgroundBase,
    backgroundBrandBase = backgroundBrandBase,
    backgroundSecondary = backgroundSecondary,
    backgroundTertiary = backgroundTertiary,
    borderDisabled = borderDisabled,
    borderFilled = borderFilled,
    borderWhite = borderWhite,
    borderError = borderError,
    buttonActive = buttonActive,
    buttonDisabled = buttonDisabled,
    buttonSecondary = buttonSecondary,
    buttonTertiary = buttonTertiary,
    buttonDisabledTertiary = buttonDisabledTertiary,
    iconWhite = iconWhite,
    iconBase = iconBase,
    iconSecondary = iconSecondary,
    iconDisabled = iconDisabled,
    iconRed = iconRed,
    iconSubtle = iconSubtle,
    pinkSun = pinkSun,
    splashBackground = splashBackground,
    sunsetNight = sunsetNight,
    color1 = color1,
    color2 = color2,
    color3 = color3,
    color4 = color4,
    color5 = color5
)

fun dark(
    textBase: Color = DarkTextBase,
    textSubtle: Color = DarkTextSubtle,
    textLink: Color = DarkTextLink,
    textRed: Color = DarkTextRed,
    textWhite: Color = DarkTextWhite,
    backgroundBase: Color = DarkBackgroundBase,
    backgroundBrandBase: Color = DarkBackgroundBrandBase,
    backgroundSecondary: Color = DarkBackgroundSecondary,
    backgroundTertiary: Color = DarkBackgroundTertiary,
    borderDisabled: Color = DarkBorderDisabled,
    borderFilled: Color = DarkBorderFilled,
    borderWhite: Color = DarkBorderWhite,
    borderError: Color = DarkBorderError,
    buttonActive: Color = DarkButtonActive,
    buttonDisabled: Color = DarkButtonDisabled,
    buttonSecondary: Color = DarkButtonSecondary,
    buttonTertiary: Color = DarkButtonTertiary,
    buttonDisabledTertiary: Color = DarkButtonDisabledTertiary,
    iconWhite: Color = DarkIconWhite,
    iconBase: Color = DarkIconBase,
    iconSecondary: Color = DarkIconSecondary,
    iconDisabled: Color = DarkIconDisabled,
    iconRed: Color = DarkIconRed,
    iconSubtle: Color = DarkIconSubtle,
    pinkSun: Color = PinkSun,
    splashBackground: Brush = SplashBackground,
    sunsetNight: Brush = SunsetNight,
    color1: Color = Color1,
    color2: Color = Color2,
    color3: Color = Color3,
    color4: Color = Color4,
    color5: Color = Color5
) = ColorScheme(
    textBase = textBase,
    textSubtle = textSubtle,
    textLink = textLink,
    textRed = textRed,
    textWhite = textWhite,
    backgroundBase = backgroundBase,
    backgroundBrandBase = backgroundBrandBase,
    backgroundSecondary = backgroundSecondary,
    backgroundTertiary = backgroundTertiary,
    borderDisabled = borderDisabled,
    borderFilled = borderFilled,
    borderWhite = borderWhite,
    borderError = borderError,
    buttonActive = buttonActive,
    buttonDisabled = buttonDisabled,
    buttonSecondary = buttonSecondary,
    buttonTertiary = buttonTertiary,
    buttonDisabledTertiary = buttonDisabledTertiary,
    iconWhite = iconWhite,
    iconBase = iconBase,
    iconSecondary = iconSecondary,
    iconDisabled = iconDisabled,
    iconRed = iconRed,
    iconSubtle = iconSubtle,
    pinkSun = pinkSun,
    splashBackground = splashBackground,
    sunsetNight = sunsetNight,
    color1 = color1,
    color2 = color2,
    color3 = color3,
    color4 = color4,
    color5 = color5
)

val LocalColorScheme = staticCompositionLocalOf { light() }

// Alias for backward compatibility
val LocalCustomColorScheme = LocalColorScheme
