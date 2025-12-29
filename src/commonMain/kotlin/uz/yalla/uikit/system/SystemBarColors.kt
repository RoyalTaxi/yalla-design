package uz.yalla.uikit.system

import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

/**
 * Sets the system bar (status bar and navigation bar) icon colors.
 *
 * @param statusBarColor The background color of the status bar to determine icon colors
 * @param navigationBarColor The background color of the navigation bar to determine icon colors
 */
@Composable
expect fun SystemBarColors(
    statusBarColor: Color,
    navigationBarColor: Color = statusBarColor
)

/**
 * Sets the system bar (status bar and navigation bar) icon colors.
 *
 * @param darkIcons Whether to use dark icons (for light backgrounds)
 */
@Composable
expect fun SystemBarColors(darkIcons: Boolean)
