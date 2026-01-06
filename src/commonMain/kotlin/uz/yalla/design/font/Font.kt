package uz.yalla.design.font

import androidx.compose.runtime.Composable
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.sp
import org.jetbrains.compose.resources.Font
import org.jetbrains.compose.resources.FontResource
import uz.yalla.resources.Res
import uz.yalla.resources.nummernschild

expect val boldFont: FontResource
expect val mediumFont: FontResource
expect val normalFont: FontResource

@Composable
fun rememberFontScheme(): FontScheme {
    return FontScheme(
        title = FontScheme.Title(
            xLarge = TextStyle(
                fontSize = 30.sp,
                lineHeight = 30.sp,
                fontFamily = FontFamily(Font(boldFont))
            ),
            large = TextStyle(
                fontSize = 22.sp,
                lineHeight = 22.sp,
                fontFamily = FontFamily(Font(boldFont))
            ),
            base = TextStyle(
                fontSize = 20.sp,
                lineHeight = 20.sp,
                fontFamily = FontFamily(Font(boldFont))
            )
        ),
        body = FontScheme.Body(
            caption = TextStyle(
                fontSize = 13.sp,
                lineHeight = 15.6.sp,
                fontFamily = FontFamily(Font(mediumFont))
            ),
            large = FontScheme.Body.Weighty(
                regular = TextStyle(
                    fontSize = 18.sp,
                    lineHeight = 21.6.sp,
                    fontFamily = FontFamily(Font(normalFont))
                ),
                medium = TextStyle(
                    fontSize = 18.sp,
                    lineHeight = 21.6.sp,
                    fontFamily = FontFamily(Font(mediumFont))
                ),
                bold = TextStyle(
                    fontSize = 18.sp,
                    lineHeight = 21.6.sp,
                    fontFamily = FontFamily(Font(boldFont))
                )
            ),
            base = FontScheme.Body.Weighty(
                regular = TextStyle(
                    fontSize = 16.sp,
                    lineHeight = 20.8.sp,
                    fontFamily = FontFamily(Font(normalFont))
                ),
                medium = TextStyle(
                    fontSize = 16.sp,
                    lineHeight = 20.8.sp,
                    fontFamily = FontFamily(Font(mediumFont))
                ),
                bold = TextStyle(
                    fontSize = 16.sp,
                    lineHeight = 20.8.sp,
                    fontFamily = FontFamily(Font(boldFont))
                )
            ),
            small = FontScheme.Body.Weighty(
                regular = TextStyle(
                    fontSize = 14.sp,
                    lineHeight = 15.4.sp,
                    fontFamily = FontFamily(Font(normalFont))
                ),
                medium = TextStyle(
                    fontSize = 14.sp,
                    lineHeight = 15.4.sp,
                    fontFamily = FontFamily(Font(mediumFont))
                ),
                bold = TextStyle(
                    fontSize = 14.sp,
                    lineHeight = 15.4.sp,
                    fontFamily = FontFamily(Font(boldFont))
                )
            )
        ),
        custom = FontScheme.Custom(
            carNumber = TextStyle(
                fontSize = 12.sp,
                lineHeight = 16.sp,
                fontFamily = FontFamily(Font(Res.font.nummernschild))
            )
        )
    )
}
