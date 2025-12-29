package uz.yalla.uikit.system

import android.app.Activity
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.platform.LocalContext
import androidx.core.view.WindowCompat

@Composable
actual fun SystemBarColors(
    statusBarColor: Color,
    navigationBarColor: Color
) {
    val context = LocalContext.current

    SideEffect {
        val window = (context as? Activity)?.window ?: return@SideEffect
        val view = window.decorView
        val insetsController = WindowCompat.getInsetsController(window, view)

        val useDarkStatusBarIcons = statusBarColor.luminance() > 0.5f
        val useDarkNavigationBarIcons = navigationBarColor.luminance() > 0.5f

        insetsController.isAppearanceLightStatusBars = useDarkStatusBarIcons
        insetsController.isAppearanceLightNavigationBars = useDarkNavigationBarIcons
    }
}

@Composable
actual fun SystemBarColors(darkIcons: Boolean) {
    val context = LocalContext.current

    SideEffect {
        val window = (context as? Activity)?.window ?: return@SideEffect
        val view = window.decorView
        val insetsController = WindowCompat.getInsetsController(window, view)

        insetsController.isAppearanceLightStatusBars = darkIcons
        insetsController.isAppearanceLightNavigationBars = darkIcons
    }
}
