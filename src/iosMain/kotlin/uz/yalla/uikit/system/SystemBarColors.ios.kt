package uz.yalla.uikit.system

import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
import platform.UIKit.UIApplication
import platform.UIKit.UIStatusBarStyleDarkContent
import platform.UIKit.UIStatusBarStyleLightContent
import platform.UIKit.setStatusBarStyle

@Composable
actual fun SystemBarColors(
    statusBarColor: Color,
    navigationBarColor: Color
) {
    SideEffect {
        val useDarkIcons = statusBarColor.luminance() > 0.5f

        UIApplication.sharedApplication.setStatusBarStyle(
            if (useDarkIcons) UIStatusBarStyleDarkContent
            else UIStatusBarStyleLightContent,
            animated = true
        )
    }
}

@Composable
actual fun SystemBarColors(darkIcons: Boolean) {
    SideEffect {
        UIApplication.sharedApplication.setStatusBarStyle(
            if (darkIcons) UIStatusBarStyleDarkContent
            else UIStatusBarStyleLightContent,
            animated = true
        )
    }
}
